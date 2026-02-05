from django.core.management.base import BaseCommand
from game.models import Level


class Command(BaseCommand):
    help = 'Populates the database with sample CSS Bunny levels'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample levels...')
        
        levels_data = [
            # FLEXBOX LEVELS (1-10)
            {
                'level_number': 1,
                'title': 'The First Hop',
                'instruction': 'Welcome to Bunny Garden! Align our bunny to the end of the row to help it reach its burrow. (Short version "end" also works!)',
                'css_property': 'justify-content',
                'correct_solution': 'justify-content: flex-end;||justify-content:flex-end;||justify-content:end;||justify-content: end;||display: flex; justify-content: flex-end;||display:flex;justify-content:flex-end;||display:flex;justify-content:end;||display: flex; justify-content: end;',
                'bunny_count': 1,
                'carrot_count': 1,
                'difficulty': 'easy'
            },
            {
                'level_number': 2,
                'title': 'Center of Attention',
                'instruction': 'Bunnies love being exactly in the middle! Align them properly with their burrows in the center.',
                'css_property': 'justify-content',
                'correct_solution': 'justify-content: center;||justify-content:center;||display: flex; justify-content: center;||display:flex;justify-content:center;',
                'bunny_count': 1,
                'carrot_count': 1,
                'difficulty': 'easy'
            },
            {
                'level_number': 3,
                'title': 'The Social Bunch',
                'instruction': 'These bunnies want some personal space. Give them equal room around them as they find their burrows.',
                'css_property': 'justify-content',
                'correct_solution': 'justify-content: space-around;||justify-content:space-around;||display: flex; justify-content: space-around;||display:flex;justify-content:space-around;',
                'bunny_count': 3,
                'carrot_count': 3,
                'difficulty': 'easy'
            },
            {
                'level_number': 4,
                'title': 'The Perfect Edge',
                'instruction': 'Give them maximum space by pushing them to the very edges. Help them reach the burrows at the ends!',
                'css_property': 'justify-content',
                'correct_solution': 'justify-content: space-between;||justify-content:space-between;||display: flex; justify-content: space-between;||display:flex;justify-content:space-between;',
                'bunny_count': 2,
                'carrot_count': 2,
                'difficulty': 'easy'
            },
            {
                'level_number': 5,
                'title': 'Vertical Leap',
                'instruction': 'Bunnies can jump! Move them to the burrows at the bottom of the garden. Variations like "end" are also accepted.',
                'css_property': 'align-items',
                'correct_solution': 'align-items: flex-end;||align-items:flex-end;||align-items: end;||align-items:end;||display: flex; align-items: flex-end;||display:flex;align-items:flex-end;||display: flex; align-items: end;||display:flex;align-items:end;',
                'bunny_count': 1,
                'carrot_count': 1,
                'difficulty': 'easy'
            },
            {
                'level_number': 6,
                'title': 'Garden Zen',
                'instruction': 'Balance is key. Move the bunny to the center of both axes to find the burrow in the middle.',
                'css_property': 'justify-content, align-items',
                'correct_solution': 'justify-content: center; align-items: center;||justify-content:center;align-items:center;||align-items: center; justify-content: center;||display: flex; justify-content: center; align-items: center;||display:flex;justify-content:center;align-items:center;||display: flex; align-items: center; justify-content: center;',
                'bunny_count': 1,
                'carrot_count': 1,
                'difficulty': 'medium'
            },
            {
                'level_number': 7,
                'title': 'Backwards Bunny',
                'instruction': 'Sometimes we need to go back. Flip the row order to match the burrow layout.',
                'css_property': 'flex-direction',
                'correct_solution': 'flex-direction: row-reverse;||flex-direction:row-reverse;||display: flex; flex-direction: row-reverse;||display:flex;flex-direction:row-reverse;',
                'bunny_count': 1,
                'carrot_count': 1,
                'difficulty': 'medium'
            },
            {
                'level_number': 8,
                'title': 'The Tower',
                'instruction': 'Stack them up! Arrange the bunnies vertically towards their burrows.',
                'css_property': 'flex-direction',
                'correct_solution': 'flex-direction: column;||flex-direction:column;||display: flex; flex-direction: column;||display:flex;flex-direction:column;',
                'bunny_count': 2,
                'carrot_count': 2,
                'difficulty': 'medium'
            },
            {
                'level_number': 9,
                'title': 'Deep Corner',
                'instruction': 'The main burrow is in the bottom right! Change the direction to vertical and move them all the way to the bottom right.',
                'css_property': 'multiple',
                'correct_solution': 'flex-direction: column; justify-content: flex-end; align-items: flex-end;||flex-direction:column;justify-content:flex-end;align-items:flex-end;||flex-direction:column;justify-content:end;align-items:end;||display: flex; flex-direction: column; justify-content: flex-end; align-items: flex-end;||display:flex;flex-direction:column;justify-content:flex-end;align-items:flex-end;||display:flex;flex-direction:column;justify-content:end;align-items:end;||display: flex; flex-direction: column; justify-content: end; align-items: end;',
                'bunny_count': 1,
                'carrot_count': 1,
                'difficulty': 'hard'
            },
            {
                'level_number': 10,
                'title': 'Flex Master',
                'instruction': 'Final Flex Challenge! Align them in a column and center them in their burrows at the bottom.',
                'css_property': 'multiple',
                'correct_solution': 'flex-direction: column; justify-content: flex-end; align-items: center;||flex-direction:column;justify-content:flex-end;align-items:center;||flex-direction:column;justify-content:end;align-items:center;||display: flex; flex-direction: column; justify-content: flex-end; align-items: center;||display:flex;flex-direction:column;justify-content:flex-end;align-items:center;||display:flex;flex-direction:column;justify-content:end;align-items:center;||display: flex; flex-direction: column; justify-content: end; align-items: center;',
                'bunny_count': 2,
                'carrot_count': 2,
                'difficulty': 'hard'
            },

            # GRID LEVELS (11-20)
            {
                'level_number': 11,
                'title': 'Garden Grid Lock',
                'instruction': 'Unlock the power of Grid! Set the display mode to start organizing your burrow patches.',
                'css_property': 'display',
                'correct_solution': 'display: grid;||display:grid;',
                'bunny_count': 2,
                'carrot_count': 2,
                'difficulty': 'easy'
            },
            {
                'level_number': 12,
                'title': 'Dividing the Land',
                'instruction': 'Create two equal columns for your bunnies to reach their burrows.',
                'css_property': 'grid-template-columns',
                'correct_solution': 'display: grid; grid-template-columns: 1fr 1fr;||display:grid;grid-template-columns:1fr 1fr;||grid-template-columns: 1fr 1fr;||grid-template-columns:1fr 1fr;',
                'bunny_count': 2,
                'carrot_count': 2,
                'difficulty': 'easy'
            },
            {
                'level_number': 13,
                'title': 'The Triple Pass',
                'instruction': 'Bigger burrow field! Create 3 equal columns for the bunnies.',
                'css_property': 'grid-template-columns',
                'correct_solution': 'display: grid; grid-template-columns: repeat(3, 1fr);||display:grid;grid-template-columns:repeat(3,1fr);||display: grid; grid-template-columns: 1fr 1fr 1fr;||display:grid;grid-template-columns:1fr 1fr 1fr;||grid-template-columns: repeat(3, 1fr);||grid-template-columns:1fr 1fr 1fr;',
                'bunny_count': 3,
                'carrot_count': 3,
                'difficulty': 'easy'
            },
            {
                'level_number': 14,
                'title': 'Mind the Gap',
                'instruction': 'Give your bunnies breathing room between burrows! Add a 50px gap between the grid items.',
                'css_property': 'gap',
                'correct_solution': 'display: grid; grid-template-columns: 1fr 1fr; gap: 50px;||display:grid;grid-template-columns:1fr 1fr;gap:50px;||grid-template-columns: 1fr 1fr; gap: 50px;||gap: 50px;',
                'bunny_count': 2,
                'carrot_count': 2,
                'difficulty': 'medium'
            },
            {
                'level_number': 15,
                'title': 'Rows of Burrows',
                'instruction': 'Create 2 equal rows for your garden.',
                'css_property': 'grid-template-rows',
                'correct_solution': 'display: grid; grid-template-rows: 1fr 1fr;||display:grid;grid-template-rows:1fr 1fr;||grid-template-rows: 1fr 1fr;',
                'bunny_count': 2,
                'carrot_count': 2,
                'difficulty': 'medium'
            },
            {
                'level_number': 16,
                'title': 'Center Stage Grid',
                'instruction': 'Center items horizontally inside their grid cells to align with burrows.',
                'css_property': 'justify-items',
                'correct_solution': 'display: grid; grid-template-columns: 1fr 1fr; justify-items: center;||display:grid;grid-template-columns:1fr 1fr;justify-items:center;||justify-items: center;',
                'bunny_count': 2,
                'carrot_count': 2,
                'difficulty': 'medium'
            },
            {
                'level_number': 17,
                'title': 'Vertical Grid Alignment',
                'instruction': 'Center items vertically in cells to reach the burrows.',
                'css_property': 'align-items',
                'correct_solution': 'display: grid; grid-template-columns: 1fr 1fr; align-items: center;||display:grid;grid-template-columns:1fr 1fr;align-items:center;||align-items: center;',
                'bunny_count': 2,
                'carrot_count': 2,
                'difficulty': 'medium'
            },
            {
                'level_number': 18,
                'title': 'The Perfect Cell',
                'instruction': 'Center items both ways in a 2x2 grid to reach the hidden burrows.',
                'css_property': 'multiple',
                'correct_solution': 'display: grid; grid-template-columns: 1fr 1fr; justify-items: center; align-items: center;||display:grid;grid-template-columns:1fr 1fr;justify-items:center;align-items:center;||justify-items: center; align-items: center;',
                'bunny_count': 4,
                'carrot_count': 4,
                'difficulty': 'hard'
            },
            {
                'level_number': 19,
                'title': 'Uneven Ground',
                'instruction': 'Make the first column twice as wide as the second and add a 20px gap.',
                'css_property': 'grid-template-columns, gap',
                'correct_solution': 'display: grid; grid-template-columns: 2fr 1fr; gap: 20px;||display:grid;grid-template-columns:2fr 1fr;gap:20px;||grid-template-columns: 2fr 1fr; gap: 20px;',
                'bunny_count': 2,
                'carrot_count': 2,
                'difficulty': 'hard'
            },
            {
                'level_number': 20,
                'title': 'Grid Grandmaster',
                'instruction': 'The ultimate grid: 3 equal columns, 20px gap, and everything centered both ways!',
                'css_property': 'multiple',
                'correct_solution': 'display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; justify-items: center; align-items: center;||display:grid;grid-template-columns:repeat(3,1fr);gap:20px;justify-items:center;align-items:center;||grid-template-columns: repeat(3, 1fr); gap: 20px; justify-items: center; align-items: center;',
                'bunny_count': 3,
                'carrot_count': 3,
                'difficulty': 'hard'
            },

            # ADVANCED FLEXBOX (21-25)
            {
                'level_number': 21,
                'title': 'Bunny Wrap',
                'instruction': 'The garden is too narrow for all these bunnies! Allow them to wrap to the next line.',
                'css_property': 'flex-wrap',
                'correct_solution': 'flex-wrap: wrap;||flex-wrap:wrap;||display: flex; flex-wrap: wrap;||display:flex;flex-wrap:wrap;',
                'bunny_count': 6,
                'carrot_count': 6,
                'difficulty': 'medium'
            },
            {
                'level_number': 22,
                'title': 'Packed Rows',
                'instruction': 'Bunnies are wrapped, but they are too spread out. Pack them together in the middle of the garden.',
                'css_property': 'align-content',
                'correct_solution': 'flex-wrap: wrap; align-content: center;||flex-wrap:wrap;align-content:center;||align-content: center;||display: flex; flex-wrap: wrap; align-content: center;||display:flex;flex-wrap:wrap;align-content:center;||display: flex; flex-wrap: wrap; align-content: flex-end;||display: flex; flex-wrap: wrap; align-content: end;',
                'bunny_count': 6,
                'carrot_count': 6,
                'difficulty': 'medium'
            },
            {
                'level_number': 23,
                'title': 'The Big Bunny',
                'instruction': 'Bunnies need equal space between and around them. Balance the row for a more cohesive look.',
                'css_property': 'justify-content',
                'correct_solution': 'justify-content: space-evenly;||justify-content:space-evenly;||display: flex; justify-content: space-evenly;||display:flex;justify-content:space-evenly;',
                'bunny_count': 3,
                'carrot_count': 3,
                'difficulty': 'medium'
            },
            {
                'level_number': 24,
                'title': 'Column Reverse',
                'instruction': 'The burrows are upside down! Flip the column order to reach them.',
                'css_property': 'flex-direction',
                'correct_solution': 'flex-direction: column-reverse;||flex-direction:column-reverse;||display: flex; flex-direction: column-reverse;||display:flex;flex-direction:column-reverse;',
                'bunny_count': 2,
                'carrot_count': 2,
                'difficulty': 'medium'
            },
            {
                'level_number': 25,
                'title': 'The Ultimate Flexbox',
                'instruction': 'Combine row flipping and center both axes for the final flex challenge.',
                'css_property': 'multiple',
                'correct_solution': 'flex-direction: row-reverse; justify-content: center; align-items: center;||flex-direction:row-reverse;justify-content:center;align-items:center;||display: flex; flex-direction: row-reverse; justify-content: center; align-items: center;||display:flex;flex-direction:row-reverse;justify-content:center;align-items:center;',
                'bunny_count': 2,
                'carrot_count': 2,
                'difficulty': 'hard'
            },

            # ADVANCED GRID (26-30)
            {
                'level_number': 26,
                'title': 'Implicit Garden',
                'instruction': 'Create a grid with automatically generated rows of 100px.',
                'css_property': 'grid-auto-rows',
                'correct_solution': 'grid-auto-rows: 100px;||grid-auto-rows:100px;||display: grid; grid-auto-rows: 100px;||display:grid;grid-auto-rows:100px;',
                'bunny_count': 4,
                'carrot_count': 4,
                'difficulty': 'medium'
            },
            {
                'level_number': 27,
                'title': 'MinMax Burrows',
                'instruction': 'Make two columns that are at least 100px but can grow to fill the available space.',
                'css_property': 'minmax',
                'correct_solution': 'grid-template-columns: repeat(2, minmax(100px, 1fr));||grid-template-columns:repeat(2,minmax(100px,1fr));||display: grid; grid-template-columns: repeat(2, minmax(100px, 1fr));||display:grid;grid-template-columns:repeat(2,minmax(100px,1fr));',
                'bunny_count': 2,
                'carrot_count': 2,
                'difficulty': 'hard'
            },
            {
                'level_number': 28,
                'title': 'Auto-Fit Garden',
                'instruction': 'Fill the garden with as many 100px wide columns as will fit.',
                'css_property': 'auto-fit',
                'correct_solution': 'grid-template-columns: repeat(auto-fit, 100px);||grid-template-columns:repeat(auto-fit,100px);||display: grid; grid-template-columns: repeat(auto-fit, 100px);||display:grid;grid-template-columns:repeat(auto-fit,100px);',
                'bunny_count': 3,
                'carrot_count': 3,
                'difficulty': 'hard'
            },
            {
                'level_number': 29,
                'title': 'Grid Placement Flow',
                'instruction': 'Control the flow of items to be horizontal across columns.',
                'css_property': 'grid-auto-flow',
                'correct_solution': 'grid-auto-flow: column;||grid-auto-flow:column;||display: grid; grid-auto-flow: column;||display:grid;grid-auto-flow:column;',
                'bunny_count': 4,
                'carrot_count': 4,
                'difficulty': 'medium'
            },
            {
                'level_number': 30,
                'title': 'The Grand Garden Grid',
                'instruction': 'The final challenge! 3 equal columns, a massive 100px gap, and everything centered both ways.',
                'css_property': 'multiple',
                'correct_solution': 'grid-template-columns: repeat(3, 1fr); gap: 100px; place-items: center;||grid-template-columns:repeat(3,1fr);gap:100px;place-items:center;||grid-template-columns: repeat(3, 1fr); gap: 100px; justify-items: center; align-items: center;||display: grid; grid-template-columns: repeat(3, 1fr); gap: 100px; place-items: center;||display:grid;grid-template-columns:repeat(3,1fr);gap:100px;place-items:center;||display: grid; grid-template-columns: repeat(3, 1fr); gap: 100px; justify-items: center; align-items: center;',
                'bunny_count': 3,
                'carrot_count': 3,
                'difficulty': 'hard'
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        # Delete levels that are not in the new list
        new_level_numbers = [l['level_number'] for l in levels_data]
        deleted_count, _ = Level.objects.exclude(level_number__in=new_level_numbers).delete()
        if deleted_count > 0:
            self.stdout.write(self.style.WARNING(f'[-] Deleted {deleted_count} old levels.'))
        
        for level_data in levels_data:
            level, created = Level.objects.update_or_create(
                level_number=level_data['level_number'],
                defaults=level_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'[+] Created Level {level.level_number}: {level.title}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'[~] Updated Level {level.level_number}: {level.title}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n[SUCCESS] Done! Created {created_count} levels, updated {updated_count} levels, deleted {deleted_count} levels.'))
        self.stdout.write(self.style.SUCCESS(f'Total levels in database: {Level.objects.count()}'))

