#include <iostream>
#include <iterator>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

using std::cerr;
using std::cin;
using std::cout;
using std::endl;
using std::getline;
using std::istream;
using std::istream_iterator;
using std::istringstream;
using std::ostream;
using std::pair;
using std::string;
using std::vector;

typedef pair<size_t, size_t> interval;
typedef vector<interval> interval_list;
typedef vector<size_t> uint_list;
typedef vector<int> int_list;
typedef vector<interval_list> interval_list_list;

size_t
read_size(istream& is)
{
    size_t ans;
    is >> ans;
    return ans;
}

interval
read_interval(istream& is)
{
    size_t low;
    size_t high;
    is >> low;
    is >> high;
    return interval(low, high);
}

uint_list
read_uint_list(istream& is)
{
    return uint_list(
        istream_iterator<size_t>(is),
        istream_iterator<size_t>()
        );
}

interval_list
interval_list_of_uint_list(const uint_list& ul)
{
    interval_list ans(ul.size() / 2);
    for (size_t i = 0; i < ans.size(); ++i) {
        ans[i] = interval(ul[2 * i], ul[2 * i + 1]);
    }
    return ans;
}

interval_list
read_interval_list(istream& is)
{
    return interval_list_of_uint_list(read_uint_list(is));
}

void
print_interval(ostream& os, const interval& i)
{
    os << '(' << i.first << ' ' << i.second << ')';
}

void
print_interval_list(ostream& os, const interval_list& il)
{
    bool sep = false;
    for (const auto i : il) {
        if (sep) {
            os << ' ';
        }
        print_interval(os, i);
        sep = true;
    }
}

inline bool
intersects(const interval& a, const interval& b)
{
    return a.first <= b.second && b.first <= a.second;
}

//----------------------------------------------------------------------------

bool
intersects(const interval_list& a, const interval_list& b)
{
    for (const auto & ai : a) {
        for (const auto & bi : b) {
            if (intersects(ai, bi)) {
                return true;
            }
        }
    }
    return false;
}

uint_list
dumb_solution(const interval_list_list& genes, const interval_list_list& reads)
{
    uint_list ans(genes.size(), 0);
    int_list tmp(reads.size(), -1);

    for (size_t j = 0; j < reads.size(); ++j) {
        for (size_t i = 0; i < genes.size(); ++i) {
            if (tmp[j] == -1) {
                if (intersects(genes[i], reads[j])) {
                    tmp[j] = static_cast<int>(i);
                }
            } else if (tmp[j] != -2) {
                if (intersects(genes[i], reads[j])) {
                    tmp[j] = -2;
                }
            }
        }
    }

    for (const int i : tmp) {
        if (i >= 0) {
            ++ans[i];
        }
    }

    return ans;
}

//----------------------------------------------------------------------------

uint_list
interval_tree_solution(const interval_list& genes, const interval_list& reads)
{
    uint_list ans(genes.size());

    // TODO

    return ans;
}

//----------------------------------------------------------------------------

int
main()
{
    size_t n;
    size_t m;
    interval_list_list genes;
    interval_list_list reads;

    {
        string line;
        getline(cin, line);
        istringstream iss(line);
        iss >> n;
        iss >> m;
        // cerr << "n = " << n << ", "
        //      << "m = " << m << endl;

        genes.reserve(n);
        for (size_t i = 0; i < n; ++i) {
            string line;
            getline(cin, line);
            istringstream iss(line);
            genes.push_back(read_interval_list(iss));
            // cerr << "genes[" << i << "] = ";
            // print_interval_list(cerr, genes.back());
            // cerr << endl;
        }

        reads.reserve(m);
        for (size_t i = 0; i < m; ++i) {
            string line;
            getline(cin, line);
            istringstream iss(line);
            reads.push_back(read_interval_list(iss));
            // cerr << "reads[" << i << "] = ";
            // print_interval_list(cerr, reads.back());
            // cerr << endl;
        }
    }

    const auto ans = dumb_solution(genes, reads);
    for (const auto k : ans) {
        cout << k << endl;
    }
    return 0;
}
