// Copyright 2023 Gentoo Foundation
// Distributed under the terms of the GNU General Public License v2

#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;

class Digraph {
public:
  unordered_map<string, string> nodes;
  vector<std::string> order;

  void add(string a, string b) {
    nodes[a] = b;
    cout << "Inserted\n";
  }
  void pring() {
    for (auto a : nodes) {
      cout << a.first << a.second << std::endl;
    }
  }
};

int main() {
  Digraph digraph;
  string a = "sab";
  string b = "sdf";
  digraph.add(a, b);
  digraph.pring();
}
