package utils

import (
	"bytes"
	"fmt"
	"healo-backend/pkg/configs"
	"healo-backend/pkg/types"
	"io/ioutil"
	"net/http"

	"github.com/gofiber/fiber/v2"
)

// UserPrompt:: A function that accepts a prompt from the user.
//
// It reads the prompt and send it to prompt templates.
func UserPrompt(c *fiber.Ctx) error {
	var req types.Request

	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Cannot parse JSON"})
	}

	switch req.Type {
	case "Text":
		_, ok := req.Body.(string)
		if !ok {
			return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Body must be a string when type is Text"})
		}
		response, err := textPromptHandler(c.Body())
		if(err != nil){
			return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "response"})
		}
		return c.JSON(fiber.Map{"Type": "Text", "body": response})

	case "Form":
		body, ok := req.Body.(map[string]interface{})
		if !ok {
			return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Body must be a key-value object when type is Form"})
		}
		return c.JSON(fiber.Map{"message": "Received Form", "body": body["age"]})

	default:
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Unknown type"})
	}
}

func textPromptHandler(prompt []byte) ([]byte, error) {
	uri := getBaseModelURI()
	uri += "prompt/"

	req, err := http.NewRequest("POST", uri, bytes.NewBuffer(prompt))
	if err != nil {
		return ([]byte)("Failed to create request"), err
	}
	req.Header.Set("Content-Type", "application/json")

	// Send the request to LLM model
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return ([]byte)("Failed to create request"), err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return ([]byte)("Failed to create request"), err
	}

	// Print the response status and body
	fmt.Println("Response Status:", resp.Status)
	fmt.Println("Response Body:", string(body))
	if resp.StatusCode != 200 {
		return ([]byte)(body), err
	}
	return body, nil
}

func getBaseModelURI() string {
	llmIp := configs.EnvLLMModelIP()
	llmPort := configs.EnvLLMModelPort()
	return "http://" + llmIp + ":" + llmPort + "/"
}
