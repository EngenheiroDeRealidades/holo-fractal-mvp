# scripts/astro.py

import swisseph
import argparse
import datetime
import json
import sys

def get_transits(date: datetime.date):
    """
    Retorna os trânsitos do Sol e da Lua para a data fornecida.
    """
    # onde estão os efemérides (pode ser pasta local ephe/)
    swisseph.set_ephe_path(".")
    jd = swisseph.julday(date.year, date.month, date.day)
    sun = swisseph.calc_ut(jd, swisseph.SUN)
    moon = swisseph.calc_ut(jd, swisseph.MOON)
    return {
        "date": date.isoformat(),
        "sun":    {"longitude": sun[0], "latitude": sun[1], "distance_au": sun[2]},
        "moon":   {"longitude": moon[0], "latitude": moon[1], "distance_au": moon[2]}
    }

def main():
    parser = argparse.ArgumentParser(
        description="Calcula trânsitos de Sol e Lua para uma data específica."
    )
    parser.add_argument(
        "--date", "-d",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        default=datetime.date.today(),
        help="Data no formato AAAA-MM-DD (default: hoje)"
    )
    args = parser.parse_args()

    data = get_transits(args.date)
    # imprime um JSON clean no stdout
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")

if __name__ == "__main__":
    main()
