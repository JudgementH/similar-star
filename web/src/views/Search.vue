<template>
    <div>
        <v-layout row wrap justify-center>
            <v-image-input
                    v-model="imageData"
                    :image-quality="0.85"
                    clearable
                    image-format="jpeg"
            />
        </v-layout>
    </div>
</template>

<script>
    import VImageInput from 'vuetify-image-input'

    export default {
        name: "Search",
        components: {
            [VImageInput.name]: VImageInput,
        },

    }
</script>

<style scoped>

</style>