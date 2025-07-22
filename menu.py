import pygame
import colors


class GameState:
    """Enumeration for game states."""

    MENU = 0
    PLAYING = 1
    GAME_OVER = 2


def draw_rounded_rect(surface, color, rect, radius):
    """
    Draw a rounded rectangle on a surface.

    Args:
        surface: pygame Surface to draw on
        color: RGB color tuple
        rect: pygame Rect defining position and size
        radius: corner radius in pixels
    """
    if radius <= 0:
        pygame.draw.rect(surface, color, rect)
        return

    rounded_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(
        rounded_surf, color, (0, 0, rect.width, rect.height), border_radius=radius
    )
    surface.blit(rounded_surf, rect.topleft)


class Button:
    """Button widget with hover effects and rounded corners."""

    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        color=colors.SAGE_GREEN,
        hover_color=colors.HOVER_SAGE,
        text_color=colors.BLACK,
    ):
        """
        Initialize a button.

        Args:
            x, y: button position
            width, height: button dimensions
            text: button text
            color: default button color
            hover_color: color when hovered
            text_color: text color
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False
        self.font = pygame.font.Font(None, 48)
        self.pressed = False

    def draw(self, screen):
        """Render the button to the screen."""

        color = self.hover_color if self.hovered else self.color
        if self.pressed:
            color = tuple(max(0, c - 30) for c in color)

        draw_rounded_rect(screen, color, self.rect, 8)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        """
        Handle pygame events for button interaction.

        Args:
            event: pygame event

        Returns:
            bool: True if button was clicked, False otherwise
        """
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed and self.rect.collidepoint(event.pos):
                self.pressed = False
                return True
            self.pressed = False
        return False


class Slider:
    """A simple slider widget for pygame applications."""

    WIDTH = 200
    HEIGHT = 60
    TRACK_HEIGHT = 10
    TRACK_LENGTH = 180
    HANDLE_SIZE = 25
    FONT_SIZE = 24
    TEXT_MARGIN = 30

    def __init__(self, x, y, min_val, max_val, initial_val, label):
        """Initialize a slider widget.

        Args:
            x: X position of the slider
            y: Y position of the slider
            min_val: Minimum value of the slider
            max_val: Maximum value of the slider
            initial_val: Initial value of the slider
            label: Text label for the slider
        """
        self.x = x
        self.y = y
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.label = label
        self.dragging = False

        self.font = pygame.font.Font(None, self.FONT_SIZE)

        self.track_x = x + (self.WIDTH - self.TRACK_LENGTH) // 2
        self.track_y = y + self.TEXT_MARGIN

        self.handle_x = (
            self.track_x
            + (self.val - min_val) / (max_val - min_val) * self.TRACK_LENGTH
        )

    def draw(self, screen):
        """Draw the slider on the given screen surface.

        Args:
            screen: Pygame surface to draw on
        """
        text = self.font.render(f"{self.label}: {self.val}", True, colors.BLACK)
        screen.blit(text, (self.x + 60, self.y))

        track_rect = pygame.Rect(
            self.track_x, self.track_y, self.TRACK_LENGTH, self.TRACK_HEIGHT
        )
        pygame.draw.rect(
            screen, colors.WHITE, track_rect, border_radius=self.TRACK_HEIGHT // 2
        )

        active_width = self.handle_x - self.track_x
        if active_width > 0:
            active_rect = pygame.Rect(
                self.track_x, self.track_y, active_width, self.TRACK_HEIGHT
            )
            pygame.draw.rect(
                screen,
                colors.SAGE_GREEN,
                active_rect,
                border_radius=self.TRACK_HEIGHT // 2,
            )

        handle_color = colors.HOVER_SAGE if self.dragging else colors.SAGE_GREEN
        handle_rect = pygame.Rect(
            int(self.handle_x - self.HANDLE_SIZE // 2),
            self.track_y - (self.HANDLE_SIZE - self.TRACK_HEIGHT) // 2,
            self.HANDLE_SIZE,
            self.HANDLE_SIZE,
        )
        pygame.draw.rect(screen, handle_color, handle_rect, border_radius=4)

    def handle_event(self, event):
        """Handle pygame events for slider interaction.

        Args:
            event: Pygame event object
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_rect = pygame.Rect(
                int(self.handle_x - self.HANDLE_SIZE // 2),
                self.track_y - (self.HANDLE_SIZE - self.TRACK_HEIGHT) // 2,
                self.HANDLE_SIZE,
                self.HANDLE_SIZE,
            )
            if handle_rect.collidepoint(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x = max(
                self.track_x, min(self.track_x + self.TRACK_LENGTH, event.pos[0])
            )
            ratio = (mouse_x - self.track_x) / self.TRACK_LENGTH
            new_val = self.min_val + ratio * (self.max_val - self.min_val)
            self.val = round(new_val)
            actual_ratio = (self.val - self.min_val) / (self.max_val - self.min_val)
            self.handle_x = self.track_x + actual_ratio * self.TRACK_LENGTH


class Toggle:
    """Toggle switch widget with smooth animations."""

    FONT_SIZE = 28
    OPTION_FONT_SIZE = 24
    SWITCH_WIDTH = 80
    SWITCH_HEIGHT = 36
    HANDLE_SIZE = 28
    HANDLE_PADDING = 4
    TEXT_SPACING = 10
    ANIMATION_SPEED = 8
    BORDER_RADIUS = 8
    HANDLE_RADIUS = 6

    def __init__(self, x, y, width, height, option1, option2, initial_state=False):
        """Initialize a toggle switch.

        Args:
            x: X position of the toggle
            y: Y position of the toggle
            width: Width of the toggle area
            height: Height of the toggle area
            option1: Text for False state
            option2: Text for True state
            initial_state: Starting state (default: False)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.option1 = option1
        self.option2 = option2
        self.state = initial_state

        self.font = pygame.font.Font(None, self.FONT_SIZE)
        self.option_font = pygame.font.Font(None, self.OPTION_FONT_SIZE)

        self.switch_x = x + width // 2 - self.SWITCH_WIDTH // 2
        self.switch_y = y + height - self.SWITCH_HEIGHT - 10
        self.switch_rect = pygame.Rect(
            self.switch_x, self.switch_y, self.SWITCH_WIDTH, self.SWITCH_HEIGHT
        )

        self.animation_progress = 1.0 if initial_state else 0.0
        self.target_progress = 1.0 if initial_state else 0.0

    def update_animation(self, dt=0.016):
        """Update animation progress.

        Args:
            dt: Delta time for smooth animation
        """
        if abs(self.animation_progress - self.target_progress) > 0.01:
            self.animation_progress += (
                (self.target_progress - self.animation_progress)
                * self.ANIMATION_SPEED
                * dt
            )

    def draw(self, screen):
        """Draw the toggle on the given screen surface.

        Args:
            screen: Pygame surface to draw on
        """
        option1_text = self.option_font.render(self.option1, True, colors.BLACK)
        option2_text = self.option_font.render(self.option2, True, colors.BLACK)

        option1_rect = option1_text.get_rect(
            centery=self.switch_rect.centery,
            right=self.switch_rect.left - self.TEXT_SPACING,
        )
        option2_rect = option2_text.get_rect(
            centery=self.switch_rect.centery,
            left=self.switch_rect.right + self.TEXT_SPACING,
        )

        screen.blit(option1_text, option1_rect)
        screen.blit(option2_text, option2_rect)

        self.update_animation()

        bg_color = self._interpolate_color(
            colors.WHITE, colors.BLACK, self.animation_progress
        )
        draw_rounded_rect(screen, bg_color, self.switch_rect, self.BORDER_RADIUS)

        handle_travel = self.SWITCH_WIDTH - self.HANDLE_SIZE - (self.HANDLE_PADDING * 2)
        handle_x = (
            self.switch_rect.left
            + self.HANDLE_PADDING
            + handle_travel * self.animation_progress
        )
        handle_rect = pygame.Rect(
            int(handle_x),
            self.switch_rect.centery - self.HANDLE_SIZE // 2,
            self.HANDLE_SIZE,
            self.HANDLE_SIZE,
        )

        draw_rounded_rect(screen, colors.SAGE_GREEN, handle_rect, self.HANDLE_RADIUS)

    def _interpolate_color(self, color1, color2, t):
        """Interpolate between two colors.

        Args:
            color1: Starting RGB color
            color2: Ending RGB color
            t: Interpolation factor (0-1)

        Returns:
            tuple: Interpolated RGB color
        """
        return tuple(int(color1[i] + (color2[i] - color1[i]) * t) for i in range(3))

    def handle_event(self, event):
        """Handle pygame events for toggle interaction.

        Args:
            event: Pygame event object

        Returns:
            bool: True if toggle was clicked, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_area = pygame.Rect(
                self.rect.left,
                self.switch_y - 10,
                self.rect.width,
                self.SWITCH_HEIGHT + 20,
            )
            if self.switch_rect.collidepoint(event.pos) or click_area.collidepoint(
                event.pos
            ):
                self.state = not self.state
                self.target_progress = 1.0 if self.state else 0.0
                return True
        return False


class GameMenu:
    """Main game menu with settings and navigation."""

    def __init__(self, screen_size):
        """
        Initialize the game menu.

        Args:
            screen_size: size of the game screen
        """
        self.screen_size = screen_size
        self.title_font = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)

        center_x = screen_size // 2

        self.depth_slider = Slider(center_x - 100, 450, 1, 5, 4, "Depth ")
        self.color_toggle = Toggle(
            center_x - 150, 340, 300, 80, "White", "Black", False
        )
        self.play_button = Button(center_x - 90, 250, 180, 60, "PLAY")
        self.back_button = Button(
            30, 30, 120, 45, "Menu", color=colors.SAGE_GREEN, text_color=colors.GRAY
        )

    def draw_menu(self, screen):
        """Render the main menu screen."""
        screen.fill(colors.BACKGROUND)

        title_text = self.title_font.render("SAVANNA STRATEGY", True, colors.BLACK)
        title_rect = title_text.get_rect(center=(self.screen_size // 2, 80))

        screen.blit(title_text, title_rect)

        self.play_button.draw(screen)
        self.depth_slider.draw(screen)
        self.color_toggle.draw(screen)

    def draw_game_over(self, screen, winner):
        """
        Render the game over screen.

        Args:
            screen: pygame surface to draw on
            winner: winning player name or None

        Returns:
            Button: back to menu button for event handling
        """
        overlay = pygame.Surface((self.screen_size, self.screen_size), pygame.SRCALPHA)
        overlay.fill(colors.OVERLAY)
        screen.blit(overlay, (0, 0))

        card_width, card_height = 400, 250
        card_rect = pygame.Rect(
            self.screen_size // 2 - card_width // 2,
            self.screen_size // 2 - card_height // 2,
            card_width,
            card_height,
        )

        draw_rounded_rect(screen, colors.GRAY, card_rect, 20)

        winner_text = f"{winner.capitalize()} Wins!" if winner else "Game Over!"
        text_surface = self.font_medium.render(
            winner_text, True, colors.LIGHT_GRAY
        )
        text_rect = text_surface.get_rect(
            center=(card_rect.centerx, card_rect.centery - 30)
        )
        screen.blit(text_surface, text_rect)

        back_button = Button(
            card_rect.centerx - 100,
            card_rect.centery + 30,
            200,
            50,
            "Menu",
        )
        back_button.draw(screen)
        return back_button

    def handle_menu_events(self, event):
        """
        Handle menu events and return actions.

        Args:
            event: pygame event

        Returns:
            str or None: action string or None if no action
        """
        if self.play_button.handle_event(event):
            return "play"

        self.depth_slider.handle_event(event)
        self.color_toggle.handle_event(event)

        return None

    def get_settings(self):
        """
        Get current menu settings.

        Returns:
            dict: dictionary containing player settings
        """
        player_color = "black" if self.color_toggle.state else "white"
        ai_color = "white" if self.color_toggle.state else "black"
        return {
            "player_color": player_color,
            "ai_color": ai_color,
            "ai_depth": self.depth_slider.val,
        }
