/*
 * Sample vulnerable parser code — for demonstration purposes only.
 * Contains intentional bugs inspired by real-world browser vulnerabilities.
 */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* ---- CVE-style: heap buffer overflow in tag parsing ---- */

#define MAX_TAG_LEN 64

typedef struct {
    char name[MAX_TAG_LEN];
    char *value;
    int  ref_count;
} Attribute;

/* BUG: no bounds check on tag_name length */
int parse_tag(const char *input, char *tag_name, size_t input_len) {
    size_t i = 0;
    if (input[0] != '<') return -1;
    i = 1;
    /* copies until '>' without checking MAX_TAG_LEN */
    size_t j = 0;
    while (i < input_len && input[i] != '>') {
        tag_name[j++] = input[i++];   /* OVERFLOW: j can exceed buffer */
    }
    tag_name[j] = '\0';
    return 0;
}

/* ---- CVE-style: use-after-free in attribute handling ---- */

Attribute *create_attribute(const char *name, const char *value) {
    Attribute *attr = (Attribute *)malloc(sizeof(Attribute));
    if (!attr) return NULL;
    strncpy(attr->name, name, MAX_TAG_LEN - 1);
    attr->name[MAX_TAG_LEN - 1] = '\0';
    attr->value = strdup(value);
    attr->ref_count = 1;
    return attr;
}

void release_attribute(Attribute *attr) {
    if (--attr->ref_count <= 0) {
        free(attr->value);
        free(attr);
    }
}

/* BUG: releases attr then continues to read attr->value */
void process_attributes(const char *name, const char *value) {
    Attribute *attr = create_attribute(name, value);
    release_attribute(attr);
    /* USE-AFTER-FREE: attr is freed, but we still read it */
    printf("Processed attribute: %s\n", attr->value);
}

/* ---- CVE-style: integer overflow in size calculation ---- */

char *allocate_buffer(unsigned int count, unsigned int element_size) {
    /* BUG: multiplication can overflow for large values */
    unsigned int total = count * element_size;
    char *buf = (char *)malloc(total);
    if (!buf) return NULL;
    memset(buf, 0, total);
    return buf;
}

/* ---- CVE-style: double-free in error path ---- */

int parse_document(const char *data, size_t len) {
    char *working_copy = (char *)malloc(len + 1);
    if (!working_copy) return -1;
    memcpy(working_copy, data, len);
    working_copy[len] = '\0';

    char tag_name[MAX_TAG_LEN];
    if (parse_tag(working_copy, tag_name, len) != 0) {
        free(working_copy);
        /* fall through to second free — DOUBLE FREE */
    }

    /* ... more processing ... */

    free(working_copy);  /* BUG: may double-free if parse_tag failed */
    return 0;
}
