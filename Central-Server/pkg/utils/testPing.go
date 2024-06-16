// utils:: This package contains utilities for the backend server.
package utils

import (
	"healo-backend/pkg/types"
	"net/http"

	"github.com/gofiber/fiber/v2"
)

// Ping:: A function that returns a pong response.
func Ping(c *fiber.Ctx) error {
	return c.Status(http.StatusOK).JSON(types.Response{
		Data: &fiber.Map{"data": "pong"},
	})
}
