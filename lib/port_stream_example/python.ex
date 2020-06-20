defmodule PortStreamExample.Python do
  use GenServer

  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, nil, opts)
  end

  def collect_image!(pid) do
    GenServer.cast(pid, :collect)
  end

  def stop_collection!(pid) do
    GenServer.cast(pid, :stop_collection)
  end

  def init(_) do
    {:ok, %{port: open_port()}}
  end

  def handle_cast(:collect, state) do
    payload = Jason.encode!(%{"command" => "collect"})
    Port.command(state.port, payload)
    {:noreply, state}
  end
  def handle_cast(:stop_collection, state) do
    Port.close(state.port)
    {:noreply, %{port: open_port()}}
  end

  def handle_info({_port, {:data, bin}}, state) do
    bin
    |> :erlang.binary_to_term()
    |> Jason.decode!()
    |> handle_port_response(state)
  end

  defp handle_port_response(response, state) do
    PortStreamExampleWeb.Endpoint.broadcast "image:stream", "image_data", response
    {:noreply, state}
  end

  defp open_port do
    Port.open(
      {:spawn_executable, System.find_executable("python")},
      [:binary, :nouse_stdio, {:packet, 4}, args: ["py/image_collect.py"]]
    )
  end
end
