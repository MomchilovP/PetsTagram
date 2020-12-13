from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from accounts.decorators import user_required
from core.clean_up import clean_up_files
from pets.forms.comment_form import CommentForm
from pets.forms.pet_form import PetForm
from pets.models import Pet, Like, Comment


@login_required
def list_pets(request):
    context = {
        'pets': Pet.objects.all()
    }
    return render(request, 'pet_list.html', context)


@login_required
def details_or_comment_pet(request, pk):
    pet = Pet.objects.get(pk=pk)
    if request.method == 'GET':
        context = {
            'pet': pet,
            'form': CommentForm(),
            'can_delete': request.user == pet.user.user,
            'can_edit': request.user == pet.user.user,
            'can_like': request.user != pet.user.user,
            'has_liked': pet.like_set.filter(user_id=request.user.userprofile.id).exists(),
            'can_comment': request.user != pet.user.user,
        }
        return render(request, 'pet_detail.html', context)
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(text=form.cleaned_data['text'])
            comment.pet = pet
            comment.user = request.user.userprofile
            comment.save()
            return redirect('pet details or comment', pk)
        context = {
            'pet': pet,
            'form': form,
        }

        return render(request, 'pet_detail.html', context)


def persist_pet(request, pet, template_name):
    if request.method == 'GET':
        form = PetForm(instance=pet)
        context = {
            'form': form,
            'pet': pet,
        }
        return render(request, f'{template_name}.html', context)
    else:
        old_image = pet.image
        form = PetForm(
            request.POST,
            request.FILES,
            instance=pet
        )

        if form.is_valid():
            if old_image:
                clean_up_files(old_image.path)
            form.save()
            return redirect('pet details or comment', pet.pk)

        context = {
            'form': form,
            'pet': pet,
        }
        return render(request, f'{template_name}.html', context)


@user_required(Pet, methods=['POST'])
def edit_pet(request, pk):
    pet = Pet.objects.get(pk=pk)
    return persist_pet(request, pet, 'pet_edit')


@login_required
def create_pet(request):
    pet = Pet()
    return persist_pet(request, pet, 'pet_create')


@login_required
def delete_pet(request, pk):
    pet = Pet.objects.get(pk=pk)
    if pet.user.user != request.user:
        pass
    if request.method == 'GET':
        context = {
            'pet': pet,
        }
        return render(request, 'pet_delete.html', context)
    else:
        pet.delete()
        return redirect('list pets')


@login_required
def like_pet(request, pk):
    already_liked = Like.objects.filter(user_id=request.user.userprofile.id, pet_id=pk).first()
    if already_liked:
        already_liked.delete()
    else:
        pet = Pet.objects.get(pk=pk)
        like = Like(test=str(pk), user=request.user.userprofile)
        like.pet = pet
        like.save()
    return redirect('pet details or comment', pk)


def comment_pet(request, pk):
    pass
