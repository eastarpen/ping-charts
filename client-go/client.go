package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"github.com/sirupsen/logrus"
	"gopkg.in/yaml.v3"
	"io"
	"net"
	"net/http"
	"os"
	"reflect"
	"time"
)

const VERSION = "v1.3.1"

var (
	configFile  = flag.String("c", "client.yaml", "Client config file.")
	timeout     = flag.Int("t", 500, "Timeout, in milliseconds.")
	pack        = flag.Int("p", 10, "How many packets to send in one test.")
	showVersion = flag.Bool("version", false, "Show version.")
	clientID   int
	passw      string
	name       string
	log        *logrus.Logger

	tars       []Target
	configKeys = []string{
		"name",
		"clientId",
		"passw",
		"uploadUrl",
		"targets",
	}
	targetKeys = []string{
		"id",
		"name",
		"port",
		"addr",
	}
)

type Config struct {
	Name      string   `yaml:"name" validate:"required"`
	ClientID  int      `yaml:"clientId" validate:"required"`
	Passw     string   `yaml:"passw" validate:"required"`
	UploadURL string   `yaml:"uploadUrl" validate:"required"`
	Targets   []Target `yaml:"targets" validate:"required"`
}

type Target struct {
	ID   int    `yaml:"id" validate:"required"`
	Name string `yaml:"name" validate:"required"`
	Port int    `yaml:"port" validate:"required"`
	Addr string `yaml:"addr" validate:"required"`
}

type Data struct {
	ClientID int       `json:"clientId"`
	Passw    string    `json:"passw"`
	Name     string    `json:"name"`
	Data     []Metrics `json:"data"`
}

type Metrics struct {
	Name  string  `json:"name"`
	ID    int     `json:"id"`
	Time  int64   `json:"time"`
	Delay float64 `json:"delay"`
	Loss  float64 `json:"loss"`
}

func loadConfig(configFile string) (Config, error) {
	conf := Config{}

	data, err := os.ReadFile(configFile)

	if err != nil {
		return conf, err
	}

	if err := yaml.Unmarshal(data, &conf); err != nil {
		return conf, err
	}

	// check keys
	if err := validateStruct(conf, "Config"); err != nil {
		return conf, err
	}

	for _, value := range conf.Targets {
		if err := validateStruct(value, "Target"); err != nil {
			return conf, err
		}
	}

	return conf, nil
}

// getIPAddress takes a string parameter 'host', which can be an IP address or domain.
// If 'host' is a domain, it runs a DNS query and returns the corresponding IP address.
// If 'host' is an IP address, it returns it directly.
// If the IP of the domain does not exist, it raises an error.
func getIPAddress(host string) (string, error) {
        // Check if host is an IP address.
        if ip := net.ParseIP(host); ip != nil {
                return host, nil
        }

        // If not an IP address, assume it's a domain and do a DNS lookup.
        IPs, err := net.LookupIP(host)
        if err != nil {
                return "", fmt.Errorf("unable to resolve domain or invalid IP address: %s", host)
        }

        // Return the first resolved IP address as a string.
        return IPs[0].String(), nil
}

func tcping(host string, port int, count int, timeout time.Duration) (float64, float64, error) {
	delays := make([]float64, 0)
	lostPackets := 0

    ip, err := getIPAddress(host)
    if err != nil {
        return 0, 0, err
    }

	for i := 0; i < count; i++ {
		startTime := time.Now()
		conn, err := net.DialTimeout("tcp", fmt.Sprintf("%s:%d", ip, port), timeout)
		if err != nil {
			lostPackets++
			continue
		}
		defer conn.Close()

		endTime := time.Now()
		delay := endTime.Sub(startTime).Seconds()
		delays = append(delays, delay)
	}

	avgDelay := calculateAvgDelay(delays)
	packetLoss := float64(lostPackets) / float64(count)

	return avgDelay, packetLoss, nil
}

func calculateAvgDelay(delays []float64) float64 {
	if len(delays) == 0 {
		return 0
	}
	sum := 0.0
	for _, delay := range delays {
		sum += delay
	}

	return (sum / float64(len(delays))) * 1000
}

func sendRequest(data Data, uploadURL string) error {
	jsonData, err := json.Marshal(data)
	if err != nil {
		return fmt.Errorf("Failed to marshal data to JSON: %v", err)
	}

	resp, err := http.Post(uploadURL, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return fmt.Errorf("%v", err)
	}
	defer resp.Body.Close()

	respData, err := io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("Can not parse server response: %v", err)
	}
	log.Infof("Server response: %s", string(respData))

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("Request failed with status code: %d", resp.StatusCode)
	}

	return nil
}

func generateData(count int, timeout time.Duration) (Data, error) {
	data := Data{
		ClientID: clientID,
		Passw:    passw,
		Name:     name,
		Data:     make([]Metrics, 0),
	}

	for _, tar := range tars {
		res := Metrics{
			Name: tar.Name,
			ID:   tar.ID,
			Time: time.Now().Unix(),
		}

		delay, loss, err := tcping(tar.Addr, tar.Port, count, timeout)
        if err != nil {
            return data, err
        }
		res.Delay = delay
		res.Loss = loss

		data.Data = append(data.Data, res)
	}

	return data, nil
}

func validateStruct(s interface{}, name string) error {
	value := reflect.ValueOf(s)
	for i := 0; i < value.NumField(); i++ {
		field := value.Field(i)
		tag := value.Type().Field(i).Tag.Get("validate")
		if tag == "required" && field.IsZero() {
			yamlTag := value.Type().Field(i).Tag.Get("yaml")
			return fmt.Errorf("%s lack required field: \"%s\".", name, yamlTag)
		}
	}
	return nil
}

func main() {
	flag.Parse()

    // show version
    if *showVersion {
        fmt.Println("Ping Charts Client-go " + VERSION)
        fmt.Println("A simple tool to visualize vps latency based on TCP.")
        return
    }

	// TODO logging format
	// set up logging
	log = logrus.New()
	log.SetFormatter(&logrus.TextFormatter{
		FullTimestamp:   true,
		TimestampFormat: "2006-01-02 15:04:05",
	})


	conf, err := loadConfig(*configFile)
	if err != nil {
		log.Error(err)
		return
	}

	clientID = conf.ClientID
	passw = conf.Passw
	name = conf.Name
	tars = conf.Targets

	data, err := generateData(10, 500*time.Millisecond)
	if err != nil {
		log.Error(err)
		return
	}
	err = sendRequest(data, conf.UploadURL)
	if err != nil {
		log.Error(err)
		return
	}
}
