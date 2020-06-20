defmodule PortStreamExampleWeb.ImageChannel do
  use Phoenix.Channel

  def join("image:stream", _msg, socket) do
    {:ok, socket}
  end

  def handle_in("start_stream", _payload, socket) do
    PortStreamExample.Python.collect_image! Px
    {:noreply, socket}
  end

  def handle_in("stop_stream", _payload, socket) do
    PortStreamExample.Python.stop_collection! Px
    {:noreply, socket}
  end
end
