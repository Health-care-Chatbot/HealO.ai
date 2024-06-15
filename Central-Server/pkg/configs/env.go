package configs

import (
	"log"
	"os"

	"github.com/joho/godotenv"
)

func EnvBackendPort() string {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	return os.Getenv("BACKEND_PORT")
}


func EnvLLMModelIP() string {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	return os.Getenv("LLM_MODEL_SERVER_IP")
}


func EnvLLMModelPort() string {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	return os.Getenv("LLM_MODEL_SERVER_PORT")
}
