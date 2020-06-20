defmodule PortStreamExample.Python do
  use GenServer

  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, nil, opts)
  end

  def collect_image!(pid) do
    GenServer.cast(pid, :collect)
  end

  def init(_) do
    {:ok, %{port: open_port()}}
  end

  def handle_cast(:collect, state) do
    payload = Jason.encode!(%{"command" => "collect"})
    Port.command(state.port, payload)
    {:noreply, state}
  end

  def handle_info({_port, {:data, bin}}, state) do
    bin
    |> :erlang.binary_to_term()
    |> Jason.decode!()
    |> handle_port_response(state)
  end

  defp handle_port_response(%{"data" => _image}, state) do
    {:noreply, state}
  end
  defp handle_port_response(_, _), do: {:noreply, state}

  defp open_port do
    Port.open([
      {:spawn_executable, "python"},
      [:binary, :nouse_stdio, {:packet, 4}],
      args: ["py/image_collect.py"]
    ])
  end
end
