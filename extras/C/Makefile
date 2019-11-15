NAME = 15puzzle
SRC = ht.c main.c moves.c pq.c utils.c
OBJ = $(SRC:.c=.o)

CFLAGS += -Wall -Werror -Wextra
LDFLAGS +=

all: $(NAME)

$(NAME): $(OBJ)
	$(CC) -o $@ $(LDFLAGS) $^

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME)

re: fclean all
