#include <algorithm>
#include <cctype>
#include <iostream>
#include <iterator>
#include <string>

using std::cerr;
using std::cin;
using std::copy;
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
void
count(Iterator first, Iterator last,
      size_t& a, size_t& c, size_t& g, size_t& u)
{
    a = c = g = u = 0;
    for (; first != last; ++first) {
        a += (*first == 'A');
        c += (*first == 'C');
        g += (*first == 'G');
        u += (*first == 'U');
    }
}

template <typename Iterator>
bool
maybe_perfect(Iterator first, Iterator last)
{
    size_t a, c, g, u;
    count(first, last, a, c, g, u);
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
    if (first > last || n == 0) {
        return true;
    }
    if (! maybe_perfect(first, last)) {
        return false;
    }
    const auto c = comp(*first);
    for (auto i = 1; i < n; i += 2) {
        // cerr << "i = " << i << endl;
        if (*(first + i) == c) {
            if (is_perfect(first + 1, first + i) &&
                is_perfect(first + i + 1, last))
            {
                return true;
            }
        }
    }
    return false;
}

bool
is_perfect(const string& s, size_t begin, size_t end)
{
    const auto n = end - begin;
    if (begin > end || n == 0) {
        return true;
    }
    if (! maybe_perfect(s.begin() + begin, s.begin() + end)) {
        return false;
    }
    const auto c = comp(s[begin]);
    for (auto i = begin + 1; i < end; i += 2) {
        // cerr << "i = " << i << endl;
        if (s[i] == c) {
            if (is_perfect(s, begin + 1, i) && is_perfect(s, i + 1, end)) {
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

    size_t a, c, g, u;
    count(s.begin(), s.end(), a, c, g, u);
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
