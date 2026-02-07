# Component API Contracts: Professional UI/UX Enhancements with Animations

## UI Component Animation APIs

### TaskCard Component Contract
```
Props:
- taskId: string (required) - Unique identifier for the task
- taskData: object (required) - Task properties (title, completed, etc.)
- animationEnabled: boolean (optional, default: true) - Whether animations are active
- onToggle: function (optional) - Callback for completion toggle
- onDelete: function (optional) - Callback for deletion

Animation Behaviors:
- Mount: Fade in with scale transform (300ms)
- Toggle: Color change with subtle scale (150ms)
- Delete: Slide out with fade (250ms)
- Hover: Lift effect (200ms)

Accessibility:
- Respects prefers-reduced-motion
- Maintains keyboard navigation
- Preserves focus management
```

### TaskList Component Contract
```
Props:
- tasks: array (required) - Array of task objects
- animationEnabled: boolean (optional, default: true) - Whether animations are active
- onTaskChange: function (optional) - Callback for task updates

Animation Behaviors:
- Mount: Staggered item entrance (each item delayed by 50ms)
- Reorder: Smooth position transitions (200ms)
- Empty state: Gentle fade animation (300ms)

Accessibility:
- Respects prefers-reduced-motion
- Maintains semantic structure
- Preserves screen reader functionality
```

### ChatMessage Component Contract
```
Props:
- messageId: string (required) - Unique identifier for the message
- sender: 'user' | 'ai' (required) - Message origin
- content: string (required) - Message content
- timestamp: Date (optional) - When message was sent
- isTyping: boolean (optional, default: false) - Whether this is a typing indicator
- animationEnabled: boolean (optional, default: true) - Whether animations are active

Animation Behaviors:
- User Message: Fade in with scale (200ms)
- AI Message: Slide up from bottom (250ms)
- Typing Indicator: Continuous pulse animation (1000ms cycle)

Accessibility:
- Respects prefers-reduced-motion
- Preserves text readability
- Provides alternative feedback when animations are disabled
```

### AnimatedButton Component Contract
```
Props:
- children: ReactNode (required) - Button content
- variant: 'primary' | 'secondary' | 'icon' (optional, default: 'primary') - Button style
- size: 'small' | 'medium' | 'large' (optional, default: 'medium') - Button size
- disabled: boolean (optional, default: false) - Whether button is disabled
- animationEnabled: boolean (optional, default: true) - Whether animations are active
- onClick: function (optional) - Click handler

Animation Behaviors:
- Hover: Subtle scale or shadow (150ms)
- Active/Pressed: Compress effect (100ms)
- Disabled: No hover animation
- Focus: Visibility indicator (100ms)

Accessibility:
- Respects prefers-reduced-motion
- Maintains focus visibility
- Preserves keyboard interaction
```

### Modal Component Contract
```
Props:
- isOpen: boolean (required) - Whether modal is visible
- onClose: function (required) - Callback for closing modal
- title: string (optional) - Modal title
- children: ReactNode (required) - Modal content
- animationEnabled: boolean (optional, default: true) - Whether animations are active
- closeOnOverlayClick: boolean (optional, default: true) - Whether clicking overlay closes modal

Animation Behaviors:
- Open: Scale up with fade-in (300ms)
- Close: Scale down with fade-out (250ms)
- Overlay: Fade in/out (250ms)

Accessibility:
- Respects prefers-reduced-motion
- Maintains focus trapping
- Preserves keyboard navigation
- Proper aria attributes
```

## Animation Configuration

### Animation Presets
```
easeOutCubic: [0.215, 0.61, 0.355, 1]
easeInOutQuad: [0.455, 0.03, 0.515, 0.955]
standardDuration: 200ms
entryDuration: 300ms
exitDuration: 250ms
```

### Reduced Motion Behavior
When `prefers-reduced-motion` is enabled, animations will either:
- Be replaced with instant state changes
- Use significantly reduced duration (50ms or less)
- Maintain functionality while minimizing motion