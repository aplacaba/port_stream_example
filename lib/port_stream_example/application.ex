defmodule PortStreamExample.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  def start(_type, _args) do
    children = [
      # Start the Telemetry supervisor
      PortStreamExampleWeb.Telemetry,
      # Start the PubSub system
      {Phoenix.PubSub, name: PortStreamExample.PubSub},
      # Start the Endpoint (http/https)
      PortStreamExampleWeb.Endpoint,
      {PortStreamExample.Python, name: Px},
      # Start a worker by calling: PortStreamExample.Worker.start_link(arg)
      # {PortStreamExample.Worker, arg}
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: PortStreamExample.Supervisor]
    Supervisor.start_link(children, opts)
  end

  # Tell Phoenix to update the endpoint configuration
  # whenever the application is updated.
  def config_change(changed, _new, removed) do
    PortStreamExampleWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
