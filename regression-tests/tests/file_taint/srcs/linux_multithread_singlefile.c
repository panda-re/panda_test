#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include <fcntl.h>
#include <pthread.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

static pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
static int fd;

void *process_value1(void *unused)
{
    pthread_mutex_lock(&mutex);
    uint32_t value = 0;
    assert(lseek(fd, 0, SEEK_SET) != -1);
    ssize_t res = read(fd, &value, sizeof(value));
    assert(res != -1);
    if (value > 0x1234) {
        printf("branch 1\n");
    } else {
        printf("branch 2\n");
    }
    pthread_mutex_unlock(&mutex);
    return 0;
}

void *process_value2(void *unused)
{
    pthread_mutex_lock(&mutex);
    uint32_t value = 0;
    assert(lseek(fd, 4, SEEK_SET) != -1);
    ssize_t res = read(fd, &value, sizeof(value));
    assert(res != -1);
    if (value > 0x2345) {
        printf("branch 3\n");
    } else {
        printf("branch 4\n");
    }
    pthread_mutex_unlock(&mutex);
    return 0;
}

void *process_value3(void *unused)
{
    pthread_mutex_lock(&mutex);
    uint32_t value = 0;
    assert(lseek(fd, 8, SEEK_SET) != -1);
    ssize_t res = read(fd, &value, sizeof(value));
    assert(res != -1);
    if (value > 0x3456) {
        printf("branch 5\n");
    } else {
        printf("branch 6\n");
    }
    pthread_mutex_unlock(&mutex);
    return 0;
}

int main(int argc, char **argv)
{
    if (argc < 2) {
        printf("usage: %s <file>\n", argv[0]);
        return 0;
    }
    fd = open(argv[1], O_RDONLY);

    pthread_t threads[3];
    pthread_create(&threads[0], NULL, process_value1, NULL);
    pthread_create(&threads[1], NULL, process_value2, NULL);
    pthread_create(&threads[2], NULL, process_value3, NULL);

    for (int i = 0; i < 3; i++) {
        pthread_join(threads[i], NULL);
    }

    close(fd);

    return 0;
}
