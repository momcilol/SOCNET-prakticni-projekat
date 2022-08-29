from test.small.presentation3_test import main as pres
from test.small.balance_of_thrones import main as got
from test.random.erdos_renyi import main as er
from test.random.configuration_model import main as cm
from test.random.watts_strogatz import main as ws
from test.random.barabasi_albert import main as ba
from test.random.stochastic_block_model import main as sb
from test.real.epinions import main as ep
from test.real.slashdot import main as sd
from test.real.wiki_rfa import main as wr



test_groups = ["Small networks", "Random networks", "Large networks"]

test_labels = [
    ["Presentation network", "Game of Thrones"],
    ["Erdos Renyi", "Configuration model", "Watts Strogatz", "Barabasi Albert", "Stochastic Block Model"],
    ["Epinions", "Slashdot", "Wikipedia"]
]

tests = [
    [pres, got],
    [er, cm, ws, ba, sb],
    [ep, sd, wr]
]

def choose_test(options: list):
    ans = 0
    print("Choose type of network you want to analize: ")
    while True:
        for i in range(len(options)):
            print(f"{i}: {options[i]}")

        try:
            ans = int(input(">>"))
            if ans in range(len(options)):
                break
            else:
                print("Try again!")
        except:
            print("Try again!")
    
    return ans


def main():
    print("Welcome to network analizer!")

    ans1 = choose_test(test_groups)
    ans2 = choose_test(test_labels[ans1])

    tests[ans1][ans2]()


if __name__ == "__main__":
    main()