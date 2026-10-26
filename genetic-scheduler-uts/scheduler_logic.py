import random
import pandas as pd

class GeneticScheduler:
    def __init__(self, courses, rooms, slots, pop_size, max_gen, cx_prob, mut_prob, selection_method="Tournament", crossover_method="Single-Point"):
        self.courses = courses
        self.rooms = rooms
        self.slots = slots
        self.pop_size = pop_size
        self.max_gen = max_gen
        self.cx_prob = cx_prob
        self.mut_prob = mut_prob
        self.selection_method = selection_method
        self.crossover_method = crossover_method

    def create_individual(self):
        """Membuat satu kromosom: alokasi acak (slot, ruang) untuk setiap mata kuliah"""
        individual = []
        for course in self.courses:
            slot = random.choice(self.slots)
            # Filter ruangan yang kapasitasnya mencukupi (jika data kapasitas tersedia)
            suitable_rooms = [r for r in self.rooms if r["kapasitas"] >= course.get("kuota", 0)]
            if not suitable_rooms:
                suitable_rooms = self.rooms # Fallback jika semua kurang
            room = random.choice(suitable_rooms)
            individual.append({"slot": slot, "room": room["nama"]})
        return individual

    def calculate_fitness(self, individual):
        """
        Menghitung nilai fitness berdasarkan penalti kendala keras (hard constraints):
        1. Dosen bentrok di slot waktu yang sama.
        2. Ruangan bentrok di slot waktu yang sama.
        3. Rombel mahasiswa bentrok di slot waktu yang sama.
        4. Kapasitas ruangan tidak mencukupi kuota kelas.
        """
        penalties = 0
        
        # Buat kamus pemetaan kapasitas ruangan untuk pengecekan cepat
        room_capacity_map = {r["nama"]: r["kapasitas"] for r in self.rooms}

        for i in range(len(individual)):
            c1 = self.courses[i]
            g1 = individual[i]

            # Cek Kendala Kapasitas Ruangan
            room_cap = room_capacity_map.get(g1["room"], 999)
            class_quota = c1.get("kuota", 0)
            if room_cap < class_quota:
                penalties += 1  # Penalti jika kapasitas ruang kurang dari kuota mahasiswa

            for j in range(i + 1, len(individual)):
                c2 = self.courses[j]
                g2 = individual[j]

                # Cek jika berada di slot waktu yang sama
                if g1["slot"] == g2["slot"]:
                    # Bentrok Ruangan
                    if g1["room"] == g2["room"]:
                        penalties += 1
                    # Bentrok Dosen
                    if c1["dosen"] == c2["dosen"]:
                        penalties += 1
                    # Bentrok Rombel Mahasiswa
                    if c1["rombel"] == c2["rombel"]:
                        penalties += 1

        # Rumus Fitness: 1 / (1 + total_penalti) -> Nilai maksimal 1.0 (sempurna)
        fitness = 1.0 / (1.0 + penalties)
        return fitness

    def initialize_population(self):
        return [self.create_individual() for _ in range(self.pop_size)]

    def selection(self, population, fitnesses):
        """Memilih metode seleksi (Tournament atau Roulette Wheel)"""
        selected = []
        if self.selection_method == "Roulette Wheel":
            total_fit = sum(fitnesses)
            if total_fit == 0:
                probs = [1.0 / len(population)] * len(population)
            else:
                probs = [f / total_fit for f in fitnesses]
            
            for _ in range(len(population)):
                chosen = random.choices(population, weights=probs, k=1)[0]
                selected.append(chosen)
        else:
            # Tournament Selection (Default)
            for _ in range(len(population)):
                aspirants_idx = random.sample(range(len(population)), 3)
                best_idx = max(aspirants_idx, key=lambda idx: fitnesses[idx])
                selected.append(population[best_idx])
        return selected

    def crossover(self, parent1, parent2):
        """Memilih metode crossover (Single-Point atau Uniform)"""
        if random.random() < self.cx_prob and len(self.courses) > 2:
            if self.crossover_method == "Uniform":
                child1, child2 = [], []
                for i in range(len(self.courses)):
                    if random.random() < 0.5:
                        child1.append(parent1[i].copy())
                        child2.append(parent2[i].copy()) 
                    else:
                        child1.append(parent2[i].copy())
                        child2.append(parent1[i].copy())
                return child1, child2
            else:
                # Single-Point Crossover (Default)
                point = random.randint(1, len(self.courses) - 2)
                child1 = parent1[:point] + parent2[point:]
                child2 = parent2[:point] + parent1[point:]
                return child1, child2
        return parent1.copy(), parent2.copy()

    def mutation(self, individual):
        """Random Mutation"""
        mutated = []
        room_names = [r["nama"] for r in self.rooms]
        for i, gene in enumerate(individual):
            if random.random() < self.mut_prob:
                slot = random.choice(self.slots)
                room = random.choice(room_names)
                mutated.append({"slot": slot, "room": room})
            else:
                mutated.append(gene.copy())
        return mutated

    def run(self, progress_bar, status_text):
        population = self.initialize_population()
        best_overall_fitness = -1
        best_individual = None
        history_best = []
        history_avg = []
        solution_found_gen = None

        for gen in range(self.max_gen):
            fitnesses = [self.calculate_fitness(ind) for ind in population]
            
            max_fit = max(fitnesses)
            avg_fit = sum(fitnesses) / len(fitnesses)
            history_best.append(max_fit)
            history_avg.append(avg_fit)

            best_idx = fitnesses.index(max_fit)
            if max_fit > best_overall_fitness:
                best_overall_fitness = max_fit
                best_individual = population[best_idx]

            if max_fit == 1.0 and solution_found_gen is None:
                solution_found_gen = gen

            progress_bar.progress((gen + 1) / self.max_gen)
            status_text.text(f"Generasi {gen + 1}/{self.max_gen} | Fitness Terbaik: {max_fit:.4f}")

            if max_fit == 1.0:
                break

            selected = self.selection(population, fitnesses)
            next_population = [best_individual.copy()] # Elitisme

            while len(next_population) < self.pop_size:
                p1, p2 = random.sample(selected, 2)
                c1, c2 = self.crossover(p1, p2)
                next_population.append(self.mutation(c1))
                if len(next_population) < self.pop_size:
                    next_population.append(self.mutation(c2))

            population = next_population

        return best_individual, best_overall_fitness, history_best, history_avg, solution_found_gen
