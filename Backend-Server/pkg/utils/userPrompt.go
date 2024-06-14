package utils

import (
	"healo-backend/pkg/types"
	"net/http"

	"github.com/gofiber/fiber/v2"
)

// UserPrompt:: A function that accepts a prompt from the user.
//
// It reads the prompt and send it to prompt templates.
func UserPrompt(c *fiber.Ctx) error {
	var userPrompt types.UserPrompt
	if err := c.BodyParser(&userPrompt); err != nil {
		return c.Status(http.StatusBadRequest).JSON(types.Response{
			Status:  http.StatusBadRequest,
			Message: "error",
			Data:    &fiber.Map{"data": err.Error()},
		})
	}
	return nil
}
