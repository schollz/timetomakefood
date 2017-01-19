package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/BurntSushi/toml"
)

type reactions struct {
	Reaction []reaction
}

type reaction struct {
	Description       string
	AlternativeOrigin string `toml:"alternative_origin"`
	Variant           string
	Ingredients       string
	Directions        string
	Products          []string
	Reactants         []string
	Time              Duration
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

	var rs reactions

	for _, file := range fileList {
		fmt.Println(file)
		var rsTemp reactions
		bData, _ := ioutil.ReadFile(file)
		if _, err := toml.Decode(string(bData), &rsTemp); err != nil {
			panic(err)
		}
		rs.Reaction = append(rs.Reaction, rsTemp.Reaction...)
		fmt.Println(rsTemp.Reaction[0].Products)
	}

	hasReactants := make(map[string]bool)
	for _, reaction := range rs.Reaction {
		for _, reactant := range reaction.Reactants {
			hasReactants[reactant] = false
		}
	}
	for _, reaction := range rs.Reaction {
		for _, product := range reaction.Products {
			if _, ok := hasReactants[product]; ok {
				hasReactants[product] = true
			}
		}
	}

	fmt.Println("\nNo reactions exist to create the following products:")
	for reactant := range hasReactants {
		if !hasReactants[reactant] {
			fmt.Println(reactant)
		}
	}

	// Produce graphviz dot
	graphviz := "digraph G {\n"
	for _, reaction := range rs.Reaction {
		graphviz += "\t{" + strings.Join(reaction.Reactants, " ") + "} -> {" + strings.Join(reaction.Products, " ") + "};\n"
	}
	graphviz += "}"
	fmt.Println(graphviz)

	ioutil.WriteFile("graphviz.dot", []byte(graphviz), 0755)
	png, err := exec.Command("dot", "-Tpng", "graphviz.dot").Output()
	if err != nil {
		panic(err)
	}
	ioutil.WriteFile("graph.png", png, 0755)
	os.Remove("graphviz.dot")
}
