package configs

import (
	"fmt"

	"github.com/gofiber/fiber/v2"
)

// InitServer() initializes the server and returns the *fiber.App object.
//
// It creates a server with the following configurations:
//
// - ServerHeader: "Backend Server"
//
// - Prefork: true
func InitServer() *fiber.App {
	config := fiber.Config{
		ServerHeader: "Backend Server",
		Prefork:      true,
	}
	app := fiber.New(config)

	port := fmt.Sprint(":", EnvBackendPort())
	err := app.Listen(port)
	if(err != nil){
		panic(err)
	}
	return app
}
