#include <cctype>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

struct Pozita { int x, y, z; };

int distanca(const Pozita& a, const Pozita& b) {
    return std::abs(a.x - b.x) + std::abs(a.y - b.y) + std::abs(a.z - b.z);
}

bool hidrofob(char aminoacidi) {
    return std::string("AVILMFWYC").find(aminoacidi) != std::string::npos;
}

int main() {
    std::string sekuenca;
    std::cout << "Shkruaj sekuencen e aminoacideve: ";
    if (!(std::cin >> sekuenca)) {
        std::cerr << "Mungon sekuenca.\n";
        return 1;
    }
    for (char& aminoacidi : sekuenca) {
        aminoacidi = static_cast<char>(std::toupper(static_cast<unsigned char>(aminoacidi)));
        if (std::string("ACDEFGHIKLMNPQRSTVWY").find(aminoacidi) == std::string::npos) {
            std::cerr << "Aminoacid i pavlefshem: " << aminoacidi << '\n';
            return 1;
        }
    }

    std::vector<Pozita> pikat = {{0, 0, 0}};
    std::cout << "Drejtimet per cdo lidhje: X/x, Y/y, Z/z (+/-).\n";
    for (std::size_t i = 1; i < sekuenca.size(); ++i) {
        char drejtimi;
        std::cout << "Lidhja " << i << ": ";
        if (!(std::cin >> drejtimi)) { std::cerr << "Mungon drejtimi.\n"; return 1; }
        Pozita p = pikat.back();
        if (drejtimi == 'X') ++p.x;
        else if (drejtimi == 'x') --p.x;
        else if (drejtimi == 'Y') ++p.y;
        else if (drejtimi == 'y') --p.y;
        else if (drejtimi == 'Z') ++p.z;
        else if (drejtimi == 'z') --p.z;
        else { std::cerr << "Drejtim i pavlefshem.\n"; return 1; }
        for (const Pozita& e_zene : pikat) {
            if (distanca(p, e_zene) == 0) { std::cerr << "Pozita eshte e zene.\n"; return 1; }
        }
        pikat.push_back(p);
    }
    int kontakte = 0;
    for (std::size_t i = 0; i < pikat.size(); ++i) {
        for (std::size_t j = i + 2; j < pikat.size(); ++j) {
            if (hidrofob(sekuenca[i]) && hidrofob(sekuenca[j]) && distanca(pikat[i], pikat[j]) == 1)
                ++kontakte;
        }
        std::cout << i + 1 << ". " << sekuenca[i] << " (" << pikat[i].x << ", "
                  << pikat[i].y << ", " << pikat[i].z << ")\n";
    }
    std::cout << "Kontakte H-H: " << kontakte << " | Energjia: " << -kontakte << '\n';
    return 0;
}
