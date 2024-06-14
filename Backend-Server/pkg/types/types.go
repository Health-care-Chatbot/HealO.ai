// types:: This package contains user defined data types for the utilities to access.
package types

import "github.com/gofiber/fiber/v2"

// Response:: A struct that defines the response format.
type Response struct {
	Status  int        `json:"status"`
	Message string     `json:"message"`
	Data    *fiber.Map `json:"data"`
}

// UserPrompt:: A struct to recieve the user prompt in json format.
type UserPrompt struct {
	Prompt string `json:"prompt"`
}