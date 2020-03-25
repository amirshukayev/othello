/*
parses commands and executes them on a given board
*/

#include <iostream>
#include <sstream>

#include "command_engine.h"

using namespace std;

CommandEngine::CommandEngine(OthBoard& board) 
    : m_board(board)
{ }

CommandEngine::~CommandEngine()
{ }

void CommandEngine::CallCmd(std::string cmd, arguments args)
{
    if (cmd == "commands")
        _commands_cmd(args);
    
    else if (cmd == "moves")
        _legal_moves_cmd(args);
    
    else if (cmd == "play")
        _play_cmd(args);

    else if (cmd == "p")
        _play_cmd(args);
    
    else if (cmd == "reset")
        _reset_cmd(args);
    
    else if (cmd == "set_size")
        _set_size_cmd(args);

    else if (cmd == "time_limit")
        _set_time_limit_cmd(args);

    else if (cmd == "showboard")
        _show_board_cmd(args);

    else if (cmd == "s")
        _show_board_cmd(args);

    else if (cmd == "solve")
        _solve_cmd(args);

    else if (cmd == "undo")
        _undo_cmd(args);

    else if (cmd == "use_killer")
        _use_killer_cmd(args);
    
    else if (cmd == "use_ordering")
        _use_ordering_cmd(args);

    else if (cmd == "use_tt")
        _use_tt_cmd(args);
    
    else
        cout << cmd << " is not a real command" << endl;
}

void CommandEngine::Run()
{
    string cmd_line;

    while (true)
    {
        cout << endl << "=" << endl << endl;
        if (!getline(cin, cmd_line))
        {
            break;
        }
        if (cmd_line.size() < 1)
        {
            break;
        }

        istringstream iss(cmd_line);
        vector<string> tokens{istream_iterator<string>{iss},
                      istream_iterator<string>{}};

        string cmd = tokens[0];
        arguments args;
        for (int i = 1; i < tokens.size(); i++)
        {
            args.push_back(tokens[i]);
        }
        CallCmd(cmd, args);
    }
}

void CommandEngine::_commands_cmd(arguments args)
{
    cout << "all commands are: idk" << endl;
}

void CommandEngine::_legal_moves_cmd(arguments args)
{
    auto legal_moves = m_board.GetLegalMoves();
    if (legal_moves.empty())
    {
        cout << "pass" << endl;
    }
    else 
    {
        for (auto const& m : legal_moves)
        {
            cout << m_board.PointToString(m) << " ";
        }
        cout << endl;
    }
}

void CommandEngine::_play_cmd(arguments args)
{
    if (!m_board.Play(m_board.StrToPoint(args[0])))
    {
        cout << "Illegal Move" << endl;
    }
}
void CommandEngine::_reset_cmd(arguments args)
{
    m_board.Reset();
}

void CommandEngine::_set_size_cmd(arguments args)
{
    m_board.ChangeSize(stoi(args[0]));
}

void CommandEngine::_set_time_limit_cmd(arguments args)
{
}

void CommandEngine::_show_board_cmd(arguments args)
{
    std::cout << m_board.Str() << std::endl;
}

void CommandEngine::_solve_cmd(arguments args)
{

}

void CommandEngine::_undo_cmd(arguments args)
{
    m_board.Undo();
}

void CommandEngine::_use_killer_cmd(arguments args)
{

}

void CommandEngine::_use_ordering_cmd(arguments args)
{

}

void CommandEngine::_use_tt_cmd(arguments args)
{

}
