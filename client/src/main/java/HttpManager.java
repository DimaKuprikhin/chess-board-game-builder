import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import java.io.IOException;
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
    private final long userId;
    private final HttpClient client;

    HttpManager(String scheme, String host, int port) {
        this.scheme = scheme;
        this.host = host;
        this.port = port;
        this.userId = new Random(System.currentTimeMillis()).nextLong();
        this.client = HttpClient.newBuilder()
                                .version(HttpClient.Version.HTTP_1_1).build();
    }

    public String createGame(String script, String playAs) {
        URI uri;
        try {
            uri = new URI(scheme, null, host, port, "/load_script/", null, null);
        } catch(URISyntaxException ex) {
            System.out.println(ex.getMessage());
            return null;
        }
        JSONObject requestJson = new JSONObject();
        requestJson.put("script", script);
        requestJson.put("user_id", this.userId);
        HttpRequest request = HttpRequest
                .newBuilder().uri(uri)
                .POST(HttpRequest.BodyPublishers.ofString(
                        requestJson.toJSONString())).build();
        HttpResponse<String> response;
        try {
            response = client.send(request, HttpResponse.BodyHandlers.ofString());
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
            return null;
        }
        JSONParser parser = new JSONParser();
        JSONObject responseJson;
        try {
            responseJson = (JSONObject) parser.parse(response.body());
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
            return null;
        }
        System.out.println(responseJson.get("script_id"));
        return "";
    }
}
