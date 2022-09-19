import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.net.URI;
import java.net.URISyntaxException;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Random;

public class HttpManager {
    private final String scheme;
    private final String host;
    private final int port;
    private final HttpClient client;
    private final long userId;

    HttpManager(String scheme, String host, int port) {
        this.scheme = scheme;
        this.host = host;
        this.port = port;
        this.client = HttpClient.newBuilder()
                                .version(HttpClient.Version.HTTP_1_1).build();
        this.userId = (new Random(System.currentTimeMillis())).nextLong() / 2 + (1L << 62) + 1L;
    }

    private URI getURI(String path) {
        // Path component of uri is set only through the code, so we are not
        // expecting this to fail and do not check return value for null.
        try {
            return new URI(scheme, null, host, port, path, null, null);
        } catch(URISyntaxException ex) {
            Utils.showError("Ошибка", "Неверный синтакс uri.");
        }
        return null;
    }

    private JSONObject toJSON(String json) {
        // Strings for parsing are received from server, so we are not expecting
        // this to fail and do not check return value for null.
        System.out.println("Response " + json);
        JSONParser parser = new JSONParser();
        try {
            return (JSONObject) parser.parse(json);
        } catch (ParseException ex) {
            Utils.showError("Ошибка", "Неверный формат JSON");
        }
        return null;
    }

    private String sendRequest(HttpRequest request) {
        try {
            return client.send(request, HttpResponse.BodyHandlers.ofString()).body();
        } catch (Exception ex) {
            Utils.showError("Ошибка", "Не удалось отправить запрос на сервер");
        }
        return null;
    }

    public JSONObject createGame(long scriptId, String playAs) {
        URI uri = getURI("/create_game/");
        JSONObject requestJson = new JSONObject();
        requestJson.put("script_id", scriptId);
        requestJson.put("play_as", playAs);
        requestJson.put("user_id", userId);
        HttpRequest request = HttpRequest
                .newBuilder().uri(uri)
                .POST(HttpRequest.BodyPublishers.ofString(
                        requestJson.toJSONString())).build();
        String response = sendRequest(request);
        if (response == null) {
            return null;
        }
        return toJSON(response);
    }

    public JSONObject joinGame(String link) {
        URI uri = getURI("/join_by_link/");
        JSONObject requestJson = new JSONObject();
        requestJson.put("link", link);
        requestJson.put("user_id", userId);
        HttpRequest.BodyPublisher publisher = HttpRequest.BodyPublishers.ofString(
                requestJson.toJSONString());
        HttpRequest request = HttpRequest.newBuilder().uri(uri).POST(publisher).build();
        String response = sendRequest(request);
        if (response == null) {
            return null;
        }
        return toJSON(response);
    }

    public JSONObject loadScript(String script) {
        URI uri = getURI("/load_script/");
        JSONObject requestJson = new JSONObject();
        requestJson.put("script", script);
        HttpRequest request = HttpRequest.newBuilder().uri(uri).POST(HttpRequest.BodyPublishers.ofString(
                requestJson.toJSONString())).build();
        String response = sendRequest(request);
        if (response == null) {
            return null;
        }
        return toJSON(response);
    }

    public JSONObject getGameState(long gameId) {
        URI uri = getURI("/get_game_state/" + gameId + "/" + userId);
        JSONObject requestJson = new JSONObject();
        requestJson.put("game_id", gameId);
        requestJson.put("user_id", userId);
        HttpRequest request = HttpRequest.newBuilder().uri(uri).GET().build();
        String response = sendRequest(request);
        if (response == null) {
            return null;
        }
        return toJSON(response);
    }

    public JSONObject makeMove(Move move, long gameId) {
        URI uri = getURI("/make_move/");
        JSONObject requestJson = new JSONObject();
        requestJson.put("game_id", gameId);
        requestJson.put("move", move.toJSON());
        requestJson.put("user_id", userId);
        HttpRequest request = HttpRequest.newBuilder().uri(uri).POST(HttpRequest.BodyPublishers.ofString(
                requestJson.toJSONString())).build();
        String response = sendRequest(request);
        if (response == null) {
            return null;
        }
        return toJSON(response);
    }
}
