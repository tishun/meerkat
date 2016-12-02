package meerkat;

public class Response {

    private final String responseMessage;

    public Response(String responseMessage) {
        this.responseMessage = responseMessage;
    }

    public String getResponseMessage() {
        return this.responseMessage;
    }
}
