NAME = 15puzzle
SRC = heuristic.c ht.c main.c moves.c pq.c utils.c
OBJ = $(SRC:.c=.o)

CFLAGS += -O2 -Wall -Werror -Wextra
LDFLAGS += -O2

all: $(NAME)

$(NAME): $(OBJ)
	$(CC) -o $@ $(LDFLAGS) $^

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME)

re: fclean all
