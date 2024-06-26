// This file contains the routes for the backend server
// 
// Available routes:
// 
// 	- Get  :: /ping
// 
// 	- Post :: /prompt
package routes

import (
	"healo-backend/pkg/utils"

	"github.com/gofiber/fiber/v2"
)

// PingRoute:: A route that returns a pong response.
// It is to check for the server's availability.
func PingRoute(app *fiber.App) {
	app.Get("/ping", utils.Ping)
}

// PromptRoute:: A route that accepts a prompt from the user.
// Forwards its request to the utils.UserPrompt for processing.
func PromptRoute(app *fiber.App) {
	app.Post("/prompt", utils.UserPrompt)
}
// test_curl_request for /prompt/ route
// curl -X POST http://localhost:5000/prompt/ -H "Content-Type: application/json" -d '{"type": "Text", "body": "hey there!"}'
// curl -X POST http://localhost:5000/prompt/ -H "Content-Type: application/json" -d '{"type": "Form", "body": {"name": "John", "age": "12"}}'

