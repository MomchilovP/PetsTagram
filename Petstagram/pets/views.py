from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from Petstagram.core.clean_up import clean_up_files
from Petstagram.pets.forms.comment_form import CommentForm
from Petstagram.pets.forms.pet_form import PetForm
from Petstagram.pets.models import Pet, Like, Comment


class PetsListView(views.ListView):
    model = Pet
    template_name = 'pet_list.html'
    context_object_name = 'pets'


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


class CreatePetView(auth_mixins.LoginRequiredMixin, views.CreateView):
    template_name = 'pet_create.html'
    model = Pet
    form_class = PetForm

    def get_success_url(self):
        url = reverse_lazy('pet details or comment', kwargs={'pk': self.object.id})
        return url

    def form_valid(self, form):
        pet = form.save(commit=False)
        pet.user = self.request.user
        pet.save()
        return super().form_valid(form)


class UpdatePetView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    template_name = 'pet_edit.html'
    model = Pet
    form_class = PetForm

    def get_success_url(self):
        url = reverse_lazy('pet details or comment', kwargs={'pk': self.object.id})
        return url

    def form_valid(self, form):
        old_image = self.get_object().image
        if old_image:
            clean_up_files(old_image.path)
        return super().form_valid(form)


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
