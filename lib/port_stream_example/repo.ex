defmodule PortStreamExample.Repo do
  use Ecto.Repo,
    otp_app: :port_stream_example,
    adapter: Ecto.Adapters.Postgres
end
