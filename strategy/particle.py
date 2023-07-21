import random
import numpy as np
import cv2
from model.test_tf import *
from laserBeam.super_simulation import *
import keras.backend as bk
from laserBeam.theta import *
import copy
from utils import write_log

threshold = 0.05


class Particle:
    def __init__(self, image, lst):
        self.theta = Vector(lst)
        self.velocity = random.choice(Q).copy()
        self.best_theta = copy.copy(self.theta)
        self.image = image
        self.argmax = ''
        self.conf = 0
        self.conf_sec = 0

    def update_velocity(self, global_best_theta, inertia_weight, cognitive_weight, social_weight):
        for i in range(4):
            self.velocity[i] *= inertia_weight
        theta1 = (self.best_theta - self.theta) * cognitive_weight
        theta2 = (global_best_theta - self.theta) * social_weight
        self.velocity[0] += random.uniform(0, 1) * theta1.phi + random.uniform(0, 1) * theta2.phi
        self.velocity[1] += random.uniform(0, 1) * theta1.l + random.uniform(0, 1) * theta2.l
        self.velocity[2] += random.uniform(0, 1) * theta1.b + random.uniform(0, 1) * theta2.b
        self.velocity[3] += random.uniform(0, 1) * theta1.w + random.uniform(0, 1) * theta2.w
        self.velocity[4] += random.uniform(0, 1) * theta1.alpha + random.uniform(0, 1) * theta2.alpha

    def update_theta(self):
        self.theta.phi += self.velocity[0]
        self.theta.l += self.velocity[1]
        self.theta.b += self.velocity[2]
        self.theta.w += self.velocity[3]
        self.theta.alpha += self.velocity[4]
        self.theta.clip(self.image)


class ParticleSwarmOptimization:
    def __init__(self, image, num_particles, inertia_weight, cognitive_weight, social_weight,
                 max_iterations):
        self.num_particles = num_particles
        self.image = image
        self.inertia_weight = inertia_weight
        self.cognitive_weight = cognitive_weight
        self.social_weight = social_weight
        self.max_iterations = max_iterations
        self.particles = []
        self.label, self.conf = get_conf(image)[0]
        self.atk_times = 0
        print('[adv开始] label:%s conf:%f' % (self.label, self.conf))

    def latin_hypercube_sampling(self, dimension, num_samples):
        # 生成初始的拉丁超立方采样矩阵
        initial_matrix = [[(i + random.random()) / num_samples for i in range(num_samples)] for _ in range(dimension)]

        # 对每一列进行随机置换
        for i in range(dimension):
            random.shuffle(initial_matrix[i])

        # 对每一列进行归一化，得到最终的拉丁超立方采样样本
        samples = [[initial_matrix[i][j] for i in range(dimension)] for j in range(num_samples)]
        for sample in samples:
            sample[0] = 380 + (750 - 380) * sample[0]
            sample[1] = -math.pi / 2 + math.pi * sample[1]
            sample[2] = self.image.size[1] * sample[2]
            sample[3] = 1 + 10 * sample[3]
            sample[4] = sample[4]
        return samples

    def initialize_particles(self):
        # 生成拉丁超立方采样样本
        samples = self.latin_hypercube_sampling(5, self.num_particles)
        for i in range(self.num_particles):
            particle = Particle(self.image, samples[i])
            self.particles.append(particle)

    def update_global_best(self):
        global_best_fitness = float('inf')
        global_best_theta = None
        for particle in self.particles:
            argmax, fitness, conf_sec = self.evaluate_fitness(particle.theta)
            particle.argmax = argmax
            particle.conf = fitness
            particle.conf_sec = conf_sec
            if argmax == self.label and fitness < global_best_fitness:
                global_best_fitness = fitness
                global_best_theta = copy.copy(particle.theta)
        print('[adv最低分数] conf:%f' % global_best_fitness)

        return global_best_theta

    def evaluate_fitness(self, theta):
        image_new = makeLB(theta, self.image)
        self.atk_times += 1
        conf_list = get_conf(image_new)
        argmax, conf_max = conf_list[0]
        conf_sec = conf_list[1][1]
        return argmax, conf_max, conf_sec

    def optimize(self):
        self.initialize_particles()
        global_best_theta = self.update_global_best()

        for _ in range(self.max_iterations):
            for particle in self.particles:
                if particle.argmax != self.label and particle.conf > particle.conf_sec + threshold:
                    print("[advLB] 标签%s被攻击为%s" % (self.label, particle.argmax))
                    print("[advLB] 参数 波长:%f 位置:(%f %f) 宽度:%f 强度:%f" % (particle.theta.phi, particle.theta.l,
                                                                       particle.theta.b, particle.theta.w,
                                                                       particle.theta.alpha))
                    saveFile = 'adv/' + str(self.label) + '--' + str(particle.argmax) + '--' + str(
                        particle.conf) + '.jpg'
                    makeLB(particle.theta, self.image).save(saveFile)
                    write_log(self.label, particle.argmax, particle.theta, self.conf, particle.conf, self.atk_times)
                    return particle.theta, self.atk_times
            for particle in self.particles:
                particle.update_velocity(global_best_theta, self.inertia_weight, self.cognitive_weight,
                                         self.social_weight)
                particle.update_theta()
                if self.atk_times % 100 == 0:
                    bk.clear_session()
            global_best_theta = self.update_global_best()
            # result_image = makeLB(global_best_theta, self.image)
            # argmax, conf = get_conf(result_image)[0]
            # if argmax != self.label and conf > self.conf + threshold:
            #     bk.clear_session()
            #     print("[advLB] 标签%s被攻击为%s" % (self.label, argmax))
            #     print("[advLB] 参数 波长:%f 位置:(%f %f) 宽度:%f 强度:%f" % (global_best_theta.phi, global_best_theta.l,
            #                                                        global_best_theta.b, global_best_theta.w,
            #                                                        global_best_theta.alpha))
            #     saveFile = 'adv/' + str(self.label) + '--' + str(argmax) + '--' + str(conf) + '.jpg'
            #     # cv2.imwrite(saveFile, np.array(result_image))
            #     result_image.save(saveFile)
            #     write_log(self.label, argmax, global_best_theta, self.conf, conf, self.atk_times)
            #     return global_best_theta
        print("[advLB] 未找到攻击样本")
        saveFile = 'adv/' + str(self.label) + '--' + str(self.conf) + '.jpg'
        self.image.save(saveFile)
        theta = None
        return theta, self.atk_times


def advLB(image, inertia_weight, num_particles, max_iterations):
    num_particles = 30
    inertia_weight = 0.7
    cognitive_weight = 1.4
    social_weight = 1.4
    max_iterations = 100

    pso = ParticleSwarmOptimization(image, num_particles, inertia_weight, cognitive_weight,
                                    social_weight, max_iterations)
    best_theta, atk_times = pso.optimize()

    return best_theta, atk_times
