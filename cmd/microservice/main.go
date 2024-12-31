package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"time"

	"github.com/paulofponciano/demo-ms-intercomunicacao/internal/web"
	"github.com/spf13/viper"
)

func init() {
	viper.AutomaticEnv()
}

func main() {
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, os.Interrupt)

	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt)
	defer cancel()

	templateData := &web.TemplateData{
		Title:           viper.GetString("TITLE"),
		ResponseTime:    time.Duration(viper.GetInt("RESPONSE_TIME")),
		ExternalCallURL: viper.GetString("EXTERNAL_CALL_URL"),
		ExternalCallMethod: viper.GetString("EXTERNAL_CALL_METHOD"),
	}
	server := web.NewServer(templateData)
	router := server.CreateServer()

	go func() {
		log.Println("Starting server on port", viper.GetString("HTTP_PORT"))
		if err := http.ListenAndServe(viper.GetString("HTTP_PORT"), router); err != nil {
			log.Fatal(err)
		}
	}()

	select {
	case <-sigCh:
		log.Println("Shutting down gracefully, CTRL+C pressed...")
	case <-ctx.Done():
		log.Println("Shutting down due to other reason...")
	}

	_, shutdownCancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer shutdownCancel()
}