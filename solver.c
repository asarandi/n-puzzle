#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdlib.h>

#define MIN_FILE_SIZE   10

int badfile(int fd)
{
    (void)close(fd);
    return (-1);
}

int count_lines_in_file(char *fn)
{
    int         fd;
    int         res;
    struct stat st;
    char        buf;

    if ((fd = open(fn, O_RDONLY)) == -1)
        return (-1);
    if ((fstat(fd, &st)) != 0)
        return (badfile(fd));
    if (!(st.st_mode & S_IFREG) || (st.st_size < MIN_FILE_SIZE))
        return (badfile(fd));
    res = 0;
    while (read(fd, &buf, 1) > 0)
    {
        if (buf == '\n')
            res += 1;
    }
    (void)close(fd);
    return (res);
}

int main(int ac, char **av)
{
    if (ac > 1)
    {
        printf("%d\n", count_lines_in_file(av[1]));

    }
    else
    {
        printf("usage: %s <input.file>\n", av[0]);
    }
    return (0);
}
