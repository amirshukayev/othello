othello: oth_board.o command_engine.o main.o oth_player_ab.o
	g++ -O3 -std=c++11 -o othello oth_board.o command_engine.o main.o oth_player_ab.o

compile: oth_board.o command_engine.o main.o oth_player_ab.o

main.o: main.cpp command_engine.o oth_board.o oth_player_ab.o
	g++ -O3 -std=c++11 -c main.cpp

oth_player_ab.o: oth_board.o oth_player_ab.cpp oth_player_ab.h
	g++ -O3 -std=c++11 -c oth_player_ab.cpp

command_engine.o: command_engine.cpp command_engine.h oth_board.o
	g++ -O3 -std=c++11 -I./ -c command_engine.cpp

oth_board.o: oth_board.cpp oth_board.h
	g++ -O3 -std=c++11 -c oth_board.cpp

clean:
	rm -rf *.gch a.out *.o othello