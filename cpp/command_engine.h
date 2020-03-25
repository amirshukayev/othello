/*
parses commands and executes them on a given board
*/

#ifndef COMMAND_ENGINE_H
#define COMMAND_ENGINE_H

#include "oth_board.h"

#include <vector>
#include <string>
#include <iostream>
#include <unordered_map>

#define SUCCEED 1

typedef std::vector<std::string> arguments;

class CommandEngine; // forward definition for the cmd map
typedef void (CommandEngine::*CmdFunc)(arguments);
typedef std::unordered_map<std::string, CmdFunc> CmdMap;

class CommandEngine
{
public:
    CommandEngine(OthBoard& board);
    ~CommandEngine();

    void Run();

private:
    void CallCmd(std::string str, arguments args);

    void _commands_cmd(arguments args);
    void _legal_moves_cmd(arguments args);
    void _play_cmd(arguments args);
    void _reset_cmd(arguments args);
    void _set_size_cmd(arguments args);
    void _set_time_limit_cmd(arguments args);
    void _show_board_cmd(arguments args);
    void _solve_cmd(arguments args);
    void _undo_cmd(arguments args);
    void _use_killer_cmd(arguments args);
    void _use_ordering_cmd(arguments args);
    void _use_tt_cmd(arguments args);

private:
    OthBoard m_board;
};

#endif
