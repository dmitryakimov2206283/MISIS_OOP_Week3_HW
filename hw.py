"""
1. Создать несколько объектов классов Player, Enemy и Item с разными параметрами
2. Реализовать и запустить игровой цикл, используя предоставленный шаблон
3. Добавить новый класс Boss, который наследуется от Enemy, но имеет специальные способности:
    Особая атака, наносящая больше урона
    Больше здоровья и возможность восстанавливать здоровье
    Способность вызывать союзников (генерировать новых врагов)

4. Проанализировать и объяснить, что произойдет, если изменить порядок наследования в классе Character с (GameObject, Movable) на (Movable, GameObject) и почему
"""

from abc import ABC, abstractmethod
import random

# Базовые абстрактные классы
class GameObject(ABC):
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
    
    @abstractmethod
    def update(self):
        pass
    
    def __str__(self):
        return f"{self.name} at ({self.x}, {self.y})"

class Movable(ABC):
    @abstractmethod
    def move(self, dx, dy):
        pass

# Наследники от базовых классов
class Character(GameObject, Movable):
    """
    Если изменить наследование с (GameObject, Movable) на (Movable, GameObject) то в работе программы ничего не изменится.
    Она будет запускаться так же корректно как и до изменения наследования. Благодаря разрешению методов (MRO) python определит,
    что в строке super().__init__(x, y, name) нужно вызвать конструктор класса GameObject. Так как данный конструктор имеет сигнатуру, 
    отличную от класса Movable (что делает его уникальным в рамках линеаризации класса) во время разрешения методов он будет разрешен
    корректно.

    Однако, стоит отметить что изменение наследования повлияет на линеаризацию классов следующим образом:
        (GameObject, Movable): Character -> GameObject -> Movable
        (Movable, GameObject): Character -> Movable -> GameObject

    Другими словами, во время разрешения методов их поиск будет производиться сначала в классе Movable и только затем в классе GameObject.
    """
    def __init__(self, x, y, name, health):
        super().__init__(x, y, name)
        self.health = health
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        print(f"{self.name} moved to ({self.x}, {self.y})")
    
    def update(self):
        print(f"{self.name} updated, health: {self.health}")
    
    def is_alive(self):
        return self.health > 0

class Player(Character):
    def __init__(self, x, y, name, health, score=0):
        super().__init__(x, y, name, health)
        self.score = score
    
    def update(self):
        super().update()
        print(f"Player score: {self.score}")
    
    def collect_item(self, item):
        self.score += item.value
        print(f"Collected {item.name}, score: {self.score}")

class Enemy(Character):
    def __init__(self, x, y, name, health, damage):
        super().__init__(x, y, name, health)
        self.damage = damage
    
    def update(self):
        super().update()
        print(f"Enemy ready to attack with damage: {self.damage}")
    
    def attack(self, target):
        target.health -= self.damage
        print(f"{self.name} attacked {target.name} for {self.damage} damage")

class Boss(Enemy):
    def __init__(self, x, y, name, health, damage):
        super().__init__(x, y, name, health, damage)
        self.health = self.health * 1.3

    def super_attack(self, target):
        target.health -= self.damage * 1.2
        print(f"{self.name} did a super attack on {target.name} for {self.damage} damage!")

    def heal(self):
        self.health += self.health * 0.2

    def summon_allies(self):
        num = random.randint(1, 3)
        allies = [self.__rand_ally() for _ in range(num)]

        return allies

    def __rand_ally(self):
        return Enemy(
            random.randint(0, 500),
            random.randint(0, 500),
            f"{self.name}'s summon",
            random.randint(8, 12),
            random.randint(3, 5)
        )


class Item(GameObject):
    def __init__(self, x, y, name, value):
        super().__init__(x, y, name)
        self.value = value
    
    def update(self):
        print(f"Item {self.name} waiting to be collected")

# Базовый игровой цикл
def game_loop(player, enemies, items, turns=5):
    print("\n=== GAME START ===\n")
    
    for turn in range(1, turns + 1):
        print(f"\n--- Turn {turn} ---")
        
        # Обновление всех объектов
        player.update()
        for enemy in enemies:
            enemy.update()
        for item in items:
            item.update()
        
        # Враги атакуют игрока
        for enemy in enemies:
            if enemy.is_alive():
                enemy.attack(player)
        
        # Проверка сбора предметов
        for item in items[:]:  # Копия списка для безопасного удаления
            if item.x == player.x and item.y == player.y:
                player.collect_item(item)
                items.remove(item)
        
        # Проверка состояния игрока
        if not player.is_alive():
            print("\nИгрок погиб! Игра окончена.")
            break
        
        # Движение игрока (для примера - случайное)
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        player.move(dx, dy)

    print("\n=== GAME END ===")
    print(f"Final score: {player.score}")
    print(f"Player health: {player.health}")



player = Player(10, 10, "Steel warrior", 100)

greatsword = Item(70, 88, "Blackmetal greatsword", 25)
healing_potion = Item(66, 88, "Healing posion", 8)

skeleton1 = Enemy(10, 40, "Skeleton", 10, 3)
skeleton2 = Enemy(24, 52, "Skeleton", 10, 3)
slime = Enemy(12, 63, "Slime", 20, 5)

game_loop(player, [skeleton1, skeleton2, slime], [greatsword, healing_potion])