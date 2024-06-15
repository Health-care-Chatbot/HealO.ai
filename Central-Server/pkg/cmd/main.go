package main

import (
	"fmt"
	"healo-backend/pkg/configs"
	"healo-backend/pkg/routes"
)

func main() {
	app := configs.InitServer()

	routes.PingRoute(app)
	routes.PromptRoute(app)

	port := fmt.Sprint(":", configs.EnvBackendPort())
	err := app.Listen(port)
	if err != nil {
		panic(err)
	}
}
