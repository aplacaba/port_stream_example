defmodule PortStreamExampleWeb.PageController do
  use PortStreamExampleWeb, :controller

  def index(conn, _params) do
    render(conn, "index.html")
  end
end
