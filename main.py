import math
import random
import pyglet

pyglet.options["shadow_window"] = False
pyglet.options["debug_gl"] = False

import pyglet.gl as gl

import shader
import player


import chunk
import world

import hit


class Window(pyglet.window.Window):
	def __init__(self, **args):
		super().__init__(**args)

		# create world

		self.world = world.World()

		# create shader

		self.shader = shader.Shader("vert.glsl", "frag.glsl")
		self.shader_sampler_location = self.shader.find_uniform(b"texture_array_sampler")
		self.shader.use()

		# pyglet stuff

		pyglet.clock.schedule_interval(self.update, 1.0 / 60)
		self.mouse_captured = False

		# player stuff

		self.player = player.Player(self.world, self.shader, self.width, self.height)

		# misc stuff - DEFAULT TO GRASS BLOCK (ID 2)

		self.holding = 2  # Grass block

	def update(self, delta_time):
		# print(f"FPS: {1.0 / delta_time}")

		if not self.mouse_captured:
			self.player.input = [0, 0, 0]

		self.player.update(delta_time)

	def on_draw(self):
		self.player.update_matrices()

		# bind textures

		gl.glActiveTexture(gl.GL_TEXTURE0)
		gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, self.world.texture_manager.texture_array)
		gl.glUniform1i(self.shader_sampler_location, 0)

		# draw stuff

		gl.glEnable(gl.GL_DEPTH_TEST)
		gl.glEnable(gl.GL_CULL_FACE)

		gl.glClearColor(0.5, 0.7, 1.0, 1.0)  # Sky blue background
		self.clear()
		self.world.draw()

		gl.glFinish()

	# input functions

	def on_resize(self, width, height):
		print(f"Resize {width} * {height}")
		gl.glViewport(0, 0, width, height)

		self.player.view_width = width
		self.player.view_height = height

	def on_mouse_press(self, x, y, button, modifiers):
		if not self.mouse_captured:
			self.mouse_captured = True
			self.set_exclusive_mouse(True)

			return

		# handle breaking/placing blocks

		def hit_callback(current_block, next_block):
			if button == pyglet.window.mouse.RIGHT:
				# RIGHT CLICK - Place grass block (or whatever is held)
				self.world.try_set_block(current_block, self.holding, self.player.collider)
			elif button == pyglet.window.mouse.LEFT:
				# LEFT CLICK - Break block
				self.world.set_block(next_block, 0)
			elif button == pyglet.window.mouse.MIDDLE:
				# MIDDLE CLICK - Pick block
				self.holding = self.world.get_block_number(next_block)

		x, y, z = self.player.position
		y += self.player.eyelevel

		hit_ray = hit.Hit_ray(self.world, self.player.rotation, (x, y, z))

		while hit_ray.distance < hit.HIT_RANGE:
			if hit_ray.step(hit_callback):
				break

	def on_mouse_motion(self, x, y, delta_x, delta_y):
		if self.mouse_captured:
			sensitivity = 0.004

			self.player.rotation[0] += delta_x * sensitivity
			self.player.rotation[1] += delta_y * sensitivity

			self.player.rotation[1] = max(-math.tau / 4, min(math.tau / 4, self.player.rotation[1]))

	def on_mouse_drag(self, x, y, delta_x, delta_y, buttons, modifiers):
		self.on_mouse_motion(x, y, delta_x, delta_y)

	def on_key_press(self, key, modifiers):
		# F11 can be pressed even when mouse is not captured
		if key == pyglet.window.key.F11:
			self.set_fullscreen(not self.fullscreen)
			return

		if not self.mouse_captured:
			return

		if key == pyglet.window.key.D:
			self.player.input[0] += 1
		elif key == pyglet.window.key.A:
			self.player.input[0] -= 1
		elif key == pyglet.window.key.W:
			self.player.input[2] += 1
		elif key == pyglet.window.key.S:
			self.player.input[2] -= 1

		elif key == pyglet.window.key.SPACE:
			self.player.input[1] += 1
		elif key == pyglet.window.key.LSHIFT:
			self.player.input[1] -= 1
		elif key == pyglet.window.key.LCTRL:
			self.player.target_speed = player.SPRINTING_SPEED

		elif key == pyglet.window.key.F:
			self.player.flying = not self.player.flying

		elif key == pyglet.window.key.G:
			# Random block selection
			self.holding = random.randint(1, len(self.world.block_types) - 1)
			print(f"Now holding: {self.world.block_types[self.holding].name}")

		elif key == pyglet.window.key.O:
			# Save world
			print("Saving world...")
			self.world.save.save()
			print("World saved!")

		elif key == pyglet.window.key.R:
			# Random teleport
			# how large is the world?

			max_y = 0

			max_x, max_z = (0, 0)
			min_x, min_z = (0, 0)

			for pos in self.world.chunks:
				x, y, z = pos

				max_y = max(max_y, (y + 1) * chunk.CHUNK_HEIGHT)

				max_x = max(max_x, (x + 1) * chunk.CHUNK_WIDTH)
				min_x = min(min_x, x * chunk.CHUNK_WIDTH)

				max_z = max(max_z, (z + 1) * chunk.CHUNK_LENGTH)
				min_z = min(min_z, z * chunk.CHUNK_LENGTH)

			# get random X & Z coordinates to teleport the player to

			x = random.randint(min_x, max_x)
			z = random.randint(min_z, max_z)

			# find height at which to teleport to, by finding the first non-air block from the top of the world

			for y in range(chunk.CHUNK_HEIGHT - 1, -1, -1):
				if not self.world.get_block_number((x, y, z)):
					continue

				self.player.teleport((x, y + 1, z))
				print(f"Teleported to {x}, {y + 1}, {z}")
				break

		elif key == pyglet.window.key.ESCAPE:
			self.mouse_captured = False
			self.set_exclusive_mouse(False)

	def on_key_release(self, key, modifiers):
		if not self.mouse_captured:
			return

		if key == pyglet.window.key.D:
			self.player.input[0] -= 1
		elif key == pyglet.window.key.A:
			self.player.input[0] += 1
		elif key == pyglet.window.key.W:
			self.player.input[2] -= 1
		elif key == pyglet.window.key.S:
			self.player.input[2] += 1

		elif key == pyglet.window.key.SPACE:
			self.player.input[1] -= 1
		elif key == pyglet.window.key.LSHIFT:
			self.player.input[1] += 1
		elif key == pyglet.window.key.LCTRL:
			self.player.target_speed = player.WALKING_SPEED


class Game:
	def __init__(self):
		self.config = gl.Config(double_buffer=True, major_version=3, minor_version=3, depth_size=16)
		self.window = Window(
			config=self.config, width=1280, height=720, caption="Minecraft Clone", resizable=True, vsync=False
		)
		
		# Maximize window at start
		self.window.maximize()

	def run(self):
		pyglet.app.run()


if __name__ == "__main__":
    try:
        print("=" * 60)
        print("IMPROVED MINECRAFT CLONE")
        print("=" * 60)
        print("Features:")
        print("  - BIGGER CHUNKS: 32x256x32")
        print("  - Enhanced terrain generation with hills and trees")
        print("  - All 93 textures available")
        print("  - Default block: Grass Block (right-click to place)")
        print()
        print("Controls:")
        print("  WASD - Move")
        print("  Space - Jump")
        print("  Left Shift - Descend (fly mode)")
        print("  Left Ctrl - Sprint")
        print("  F - Toggle fly mode")
        print("  F11 - Toggle fullscreen")
        print("  G - Random block selection")
        print("  R - Random teleport")
        print("  O - Save world")
        print("  Left Click - Break block")
        print("  Right Click - Place block")
        print("  ESC - Release mouse")
        print("=" * 60)
        
        game = Game()
        game.run()
    
    except KeyboardInterrupt:
        print("\nGame interrupted by user. Exiting...")