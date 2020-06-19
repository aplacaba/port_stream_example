# This file is responsible for configuring your application
# and its dependencies with the aid of the Mix.Config module.
#
# This configuration file is loaded before any dependency and
# is restricted to this project.

# General application configuration
use Mix.Config

config :port_stream_example,
  ecto_repos: [PortStreamExample.Repo]

# Configures the endpoint
config :port_stream_example, PortStreamExampleWeb.Endpoint,
  url: [host: "localhost"],
  secret_key_base: "vsiSOVbl1WYyEhH4g99FtOXTa5V2E6B7iUMtGs//iaXLUC3vEZFZtmaWfCQ0Y/hu",
  render_errors: [view: PortStreamExampleWeb.ErrorView, accepts: ~w(html json), layout: false],
  pubsub_server: PortStreamExample.PubSub,
  live_view: [signing_salt: "wEyj89Wq"]

# Configures Elixir's Logger
config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

# Use Jason for JSON parsing in Phoenix
config :phoenix, :json_library, Jason

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{Mix.env()}.exs"
