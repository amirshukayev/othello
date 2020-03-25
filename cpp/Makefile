othello: oth_board.o command_engine.o main.o
	g++ -std=c++11 -o othello oth_board.o command_engine.o main.o

compile: oth_board.o command_engine.o main.o

main.o: main.cpp command_engine.o oth_board.o
	g++ -std=c++11 -c main.cpp

command_engine.o: command_engine.cpp command_engine.h oth_board.o
	g++ -std=c++11 -I./ -c command_engine.cpp

oth_board.o: oth_board.cpp oth_board.h
	g++ -std=c++11 -c oth_board.cpp

clean:
	rm -rf *.gch a.out *.o