package main

import (
	"bytes"
	"fmt"
	"net/http"
	"time"

	"io/ioutil"

	"github.com/dsnet/compress/brotli"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Println(r.URL.Path)
		name := r.URL.Path[1:] + ".br"
		dat, err := ioutil.ReadFile(name)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			http.Error(w, fmt.Sprintf("Unable to open and read file : %v", err), 404)
			return
		}
		decompressed, err := brotli.NewReader(bytes.NewReader(dat), nil)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			http.Error(w, fmt.Sprintf("Error decompressing file : %v", err), 404)
			return
		}
		output, err := ioutil.ReadAll(decompressed)
		fmt.Println(output)
		http.ServeContent(w, r, name, time.Now(), bytes.NewReader(output))
	})
	http.ListenAndServe(":8080", nil)
}
