/*
 * Sample IPC message handler — intentional vulnerabilities for demo.
 * Inspired by real-world IPC serialization bugs in browser engines.
 */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdint.h>

#define MSG_MAX_SIZE 4096

typedef struct {
    uint32_t type;
    uint32_t payload_len;
    char     payload[0];  /* flexible array member */
} IPCMessage;

typedef struct {
    int    fd;
    char  *recv_buffer;
    size_t recv_buf_size;
    int    authenticated;
} IPCChannel;

/* ---- BUG: trusting attacker-controlled length field ---- */

int handle_message(IPCChannel *chan, const char *raw, size_t raw_len) {
    if (raw_len < sizeof(uint32_t) * 2) return -1;

    IPCMessage *msg = (IPCMessage *)raw;

    /* BUG: payload_len comes from untrusted input, no validation
     * against raw_len. Attacker can set payload_len > actual data. */
    char *copy = (char *)malloc(msg->payload_len);
    if (!copy) return -1;

    /* OUT-OF-BOUNDS READ: copies beyond raw buffer */
    memcpy(copy, msg->payload, msg->payload_len);

    printf("Received message type %u, %u bytes\n", msg->type, msg->payload_len);
    free(copy);
    return 0;
}

/* ---- BUG: TOCTOU race in authentication check ---- */

static int global_auth_flag = 0;

int authenticate(IPCChannel *chan, const char *token) {
    /* Simulate slow auth check */
    if (strcmp(token, "valid_token") == 0) {
        global_auth_flag = 1;
        chan->authenticated = 1;
        return 1;
    }
    return 0;
}

/* BUG: TOCTOU — checks global_auth_flag then acts on chan->authenticated
 * Another thread could modify global_auth_flag between check and use */
int privileged_action(IPCChannel *chan) {
    if (global_auth_flag) {
        /* Race window: another thread could reset global_auth_flag here */
        if (chan->authenticated) {
            printf("Executing privileged action\n");
            return 0;
        }
    }
    return -1;
}

/* ---- BUG: format string vulnerability ---- */

void log_message(const char *user_data) {
    char log_buf[256];
    /* BUG: user-controlled data used as format string */
    snprintf(log_buf, sizeof(log_buf), user_data);
    printf("%s\n", log_buf);
}

/* ---- BUG: null pointer dereference on error path ---- */

IPCChannel *create_channel(int fd) {
    IPCChannel *chan = (IPCChannel *)malloc(sizeof(IPCChannel));
    /* BUG: does not check if malloc returned NULL before use */
    chan->fd = fd;
    chan->recv_buffer = (char *)malloc(MSG_MAX_SIZE);
    chan->recv_buf_size = MSG_MAX_SIZE;
    chan->authenticated = 0;
    return chan;
}
