#include <algorithm>
#include <cctype>
#include <iostream>
#include <iterator>
#include <string>

using std::cerr;
using std::cin;
using std::copy;
using std::count;
using std::cout;
using std::endl;
using std::getline;
using std::ostream_iterator;
using std::string;

char
comp(char c)
{
    switch (c) {
    case 'A' : return 'U';
    case 'C' : return 'G';
    case 'G' : return 'C';
    case 'U' : return 'A';
    }
    return '\0';
}

template <typename Iterator>
bool
maybe_perfect(Iterator first, Iterator last)
{
    const auto a = count(first, last, 'A');
    const auto c = count(first, last, 'C');
    const auto g = count(first, last, 'G');
    const auto u = count(first, last, 'U');
    // copy(first, last, ostream_iterator<char>(cerr));
    // cerr << " " << a
    //      << " " << c
    //      << " " << g
    //      << " " << u
    //      << endl;
    return a == u && c == g;
}

template <typename Iterator>
bool
is_perfect(Iterator first, Iterator last)
{
    const auto n = last - first;
    if (n == 0) {
        return true;
    }
    if (! maybe_perfect(first, last)) {
        return false;
    }
    for (auto i = 1; i < n; i += 2) {
        // cerr << "i = " << i << endl;
        if (*(first + i) == comp(*first)) {
            if (is_perfect(first + 1, first + i) &&
                is_perfect(first + i + 1, last))
            {
                return true;
            }
        }
    }
    return false;
}

int
main()
{
    string s;

    getline(cin, s);
    for (auto &c : s) c = toupper(c);
    cerr << "s = " << s << endl
         << "n = " << s.size() << endl;

    if (s.size() % 2 == 0) {
        if (is_perfect(s.begin(), s.end())) {
            cout << "perfect" << endl;
        } else {
            cout << "imperfect" << endl;
        }
        return 0;
    }

    const auto a = count(s.begin(), s.end(), 'A');
    const auto c = count(s.begin(), s.end(), 'C');
    const auto g = count(s.begin(), s.end(), 'G');
    const auto u = count(s.begin(), s.end(), 'U');
    cerr << "a = " << a << ", "
         << "c = " << c << ", "
         << "g = " << g << ", "
         << "u = " << u << endl;

    char try_remove = '\0';
    if (a == u) {
        if ((c - g) == 1) {
            try_remove = 'C';
        } else if ((g - c) == 1) {
            try_remove = 'G';
        }
    } else if (c == g) {
        if ((a - u) == 1) {
            try_remove = 'A';
        } else if ((u - a) == 1) {
            try_remove = 'U';
        }
    }

    cerr << "try_remove = " << try_remove << endl;

    if (try_remove == '\0') {
        cout << "imperfect" << endl;
        return 0;
    }

    for (size_t p = 0, q = 0; (q = s.find(try_remove, p)) != s.npos; p = q + 1) {
        cerr << "q = " << q << endl;
        // XXX
        string t = s;
        t.erase(q, 1);
        if (is_perfect(t.begin(), t.end())) {
            cout << "almost perfect" << endl;
            return 0;
        }
    }

    cout << "imperfect" << endl;

    return 0;
}
