package main

import (
	"healo-backend/pkg/configs"
	"healo-backend/pkg/routes"
)

func main() {
	app := configs.InitServer()

	routes.PingRoute(app)
	routes.PromptRoute(app)
}
