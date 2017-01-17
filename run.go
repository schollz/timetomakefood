package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/BurntSushi/toml"
)

type Reaction struct {
	Products    []string `json:"products"`
	Reactants   []string `json:"reactants"`
	URL         string   `json:"url"`
	Ingredients string   `json:"ingredients"`
	Directions  string   `json:"directions"`
	Time        Duration `json:"time"`
}

type Duration struct {
	time.Duration
}

func (d *Duration) UnmarshalText(text []byte) error {
	var err error
	d.Duration, err = time.ParseDuration(string(text))
	return err
}

func main() {
	fmt.Println("vim-go")

	// http://stackoverflow.com/questions/6608873/file-system-scanning-in-golang
	searchDir := "./data/"

	fileList := []string{}
	err := filepath.Walk(searchDir, func(path string, f os.FileInfo, err error) error {
		if strings.Contains(path, ".toml") {
			fileList = append(fileList, path)
		}
		return nil
	})
	if err != nil {
		panic(err)
	}

	reactions := make([]Reaction, len(fileList))

	for i, file := range fileList {
		fmt.Println(file)
		bData, _ := ioutil.ReadFile(file)
		if _, err := toml.Decode(string(bData), &reactions[i]); err != nil {
			panic(err)
		}
		fmt.Printf("%+v", reactions[i].Products)
	}
}
