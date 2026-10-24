import random
import pandas as pd

class GeneticScheduler:
    def __init__(self, courses, rooms, slots, pop_size, max_gen, cx_prob, mut_prob):
        self.courses = courses
        self.rooms = rooms
        self.slots = slots
        self.pop_size = pop_size
        self.max_gen = max_gen
        self.cx_prob = cx_prob
        self.mut_prob = mut_prob

    def create_individual(self):
        """Membuat satu kromosom: alokasi acak (slot, ruang) untuk setiap mata kuliah"""
        individual = []
        for _ in range(len(self.courses)):
            slot = random.choice(self.slots)
            room = random.choice(self.rooms)
            individual.append({"slot": slot, "room": room})
        return individual

    def calculate_fitness(self, individual):
        """
        Menghitung nilai fitness berdasarkan penalti kendala keras (hard constraints).
        Kendala keras:
        1. Dosen tidak boleh mengajar di slot dan waktu yang sama pada tempat berbeda.
        2. Ruangan tidak boleh dipakai dua mata kuliah berbeda di slot yang sama.
        3. Rombel mahasiswa tidak boleh ada jadwal bentrok di slot yang sama.
        """
        penalties = 0
        
        for i in range(len(individual)):
            for j in range(i + 1, len(individual)):
                c1 = self.courses[i]
                c2 = self.courses[j]
                g1 = individual[i]
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

        # Rumus Fitness: 1 / (1 + total_penalti) -> Nilai maksimal 1.0 (sempurna tanpa pelanggaran)
        fitness = 1.0 / (1.0 + penalties)
        return fitness

    def initialize_population(self):
        return [self.create_individual() for _ in range(self.pop_size)]

    def selection(self, population, fitnesses):
        """Tournament Selection"""
        selected = []
        for _ in range(len(population)):
            aspirants_idx = random.sample(range(len(population)), 3)
            best_idx = max(aspirants_idx, key=lambda idx: fitnesses[idx])
            selected.append(population[best_idx])
        return selected

    def crossover(self, parent1, parent2):
        """Single-point Crossover"""
        if random.random() < self.cx_prob and len(self.courses) > 2:
            point = random.randint(1, len(self.courses) - 2)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        return parent1.copy(), parent2.copy()

    def mutation(self, individual):
        """Random Mutation"""
        mutated = []
        for gene in individual:
            if random.random() < self.mut_prob:
                mutated.append({
                    "slot": random.choice(self.slots),
                    "room": random.choice(self.rooms)
                })
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

            # Simpan individu terbaik
            best_idx = fitnesses.index(max_fit)
            if max_fit > best_overall_fitness:
                best_overall_fitness = max_fit
                best_individual = population[best_idx]

            # Cek jika solusi valid ditemukan (fitness == 1.0)
            if max_fit == 1.0 and solution_found_gen is None:
                solution_found_gen = gen

            # Update progress bar UI
            progress_bar.progress((gen + 1) / self.max_gen)
            status_text.text(f"Generasi {gen + 1}/{self.max_gen} | Fitness Terbaik: {max_fit:.4f}")

            if max_fit == 1.0:
                break

            # Generasi berikutnya via Seleksi, Crossover, Mutasi, dan Elitisme
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