<template>
    <div>
        <v-app-bar
                app
                color="pink"
                dense
        >

            <v-toolbar-title>Search Similar Star</v-toolbar-title>

            <v-spacer></v-spacer>

            <v-btn icon>
                <v-icon>mdi-heart</v-icon>
            </v-btn>
            <v-menu
                    open-on-hover
                    offset-y
                    bottom
            >
                <template v-slot:activator="{ on, attrs }">
                    <v-btn
                            icon
                            v-bind="attrs"
                            v-on="on"
                    >
                        <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn>
                </template>

                <v-list>
                    <v-list-item
                            v-for="(item, index) in lists"
                            :key="index"
                    >
                        <v-list-item-title>{{ item }}</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>
        </v-app-bar>

    </div>
</template>

<script>
    export default {
        name: "Nav",
        data: () => ({
            lists: [
                '学习版本',
                'Judgement',
            ],
        }),
    }
</script>

<style scoped>

</style>