package main

import (
	"crypto/rand"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/BurntSushi/toml"
)

type Ghost struct {
	Db []struct {
		Data struct {
			Posts []struct {
				ID              int         `json:"id"`
				UUID            string      `json:"uuid"`
				Title           string      `json:"title"`
				Slug            string      `json:"slug"`
				Markdown        string      `json:"markdown"`
				Mobiledoc       interface{} `json:"mobiledoc"`
				HTML            string      `json:"html"`
				Amp             interface{} `json:"amp"`
				Image           string      `json:"image"`
				Featured        int         `json:"featured"`
				Page            int         `json:"page"`
				Status          string      `json:"status"`
				Language        string      `json:"language"`
				Visibility      string      `json:"visibility"`
				MetaTitle       string      `json:"meta_title"`
				MetaDescription string      `json:"meta_description"`
				AuthorID        int         `json:"author_id"`
				CreatedAt       string      `json:"created_at"`
				CreatedBy       int         `json:"created_by"`
				UpdatedAt       string      `json:"updated_at"`
				UpdatedBy       int         `json:"updated_by"`
				PublishedAt     string      `json:"published_at"`
				PublishedBy     int         `json:"published_by"`
			} `json:"posts"`
			Tags []struct {
				ID              int         `json:"id"`
				UUID            string      `json:"uuid"`
				Name            string      `json:"name"`
				Slug            string      `json:"slug"`
				Description     interface{} `json:"description"`
				Image           interface{} `json:"image"`
				ParentID        interface{} `json:"parent_id"`
				Visibility      string      `json:"visibility"`
				MetaTitle       interface{} `json:"meta_title"`
				MetaDescription interface{} `json:"meta_description"`
				CreatedAt       string      `json:"created_at"`
				CreatedBy       int         `json:"created_by"`
				UpdatedAt       string      `json:"updated_at"`
				UpdatedBy       int         `json:"updated_by"`
			} `json:"tags"`
			PostsTags []struct {
				ID        int `json:"id"`
				PostID    int `json:"post_id"`
				TagID     int `json:"tag_id"`
				SortOrder int `json:"sort_order"`
			} `json:"posts_tags"`
		} `json:"data"`
	} `json:"db"`
}

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
		if _, err2 := toml.Decode(string(bData), &rsTemp); err != nil {
			panic(err2)
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

	var blog Ghost
	blog.Db[0].Data.Posts[0].UUID, _ = newUUID()
	bJson, _ := json.MarshalIndent(blog, "", "  ")
	fmt.Println(string(bJson))
}

// newUUID generates a random UUID according to RFC 4122
// from https://play.golang.org/p/4FkNSiUDMg
func newUUID() (string, error) {
	uuid := make([]byte, 16)
	n, err := io.ReadFull(rand.Reader, uuid)
	if n != len(uuid) || err != nil {
		return "", err
	}
	// variant bits; see section 4.1.1
	uuid[8] = uuid[8]&^0xc0 | 0x80
	// version 4 (pseudo-random); see section 4.1.3
	uuid[6] = uuid[6]&^0xf0 | 0x40
	return fmt.Sprintf("%x-%x-%x-%x-%x", uuid[0:4], uuid[4:6], uuid[6:8], uuid[8:10], uuid[10:]), nil
}
