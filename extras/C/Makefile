NAME = 15puzzle
SRC = heuristic.c ht.c main.c moves.c pq.c utils.c

CFLAGS += -O2 -Wall -Werror -Wextra
LDFLAGS += -O2

all: $(NAME)

$(NAME): $(SRC:.c=.o)
	$(CC) -o $@ $(LDFLAGS) $^

clean:
	$(RM) *.o

fclean: clean
	$(RM) $(NAME)

format:
	clang-format -i *.c *.h

tidy:
	clang-tidy *.c *.h -- $(CFLAGS)

re: fclean all
